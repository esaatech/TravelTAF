from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from payments import PaymentStatus, RedirectNeeded
from .models import CreditPayment, UserCredit, CreditTransaction
from decimal import Decimal
import stripe
from django.conf import settings
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
import json
from django.urls import reverse
from .credit_calculator import CreditCalculator
from .add_user_credit import add_credits_to_user
from dotenv import load_dotenv
from django.utils import timezone
from subscriptions.models import UserProfile  # Updated import path

import os
load_dotenv()
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  # Make sure this is the secret key
STRIPE_PUBLIC_KEY = os.getenv('STRIPE_PUBLISHABLE_KEY')

@login_required
def purchase_credits(request):
    return render(request, 'purchase.html', {
        'STRIPE_PUBLIC_KEY': STRIPE_PUBLIC_KEY
    })

@login_required
@require_POST
@csrf_protect
def process_payment(request):
    try:
        data = json.loads(request.body)
        payment_method_id = data.get('payment_method_id')
        amount = float(data.get('amount'))
        currency = data.get('currency', 'USD')

        # Get or update Stripe customer
        try:
            # Get existing profile
            user_profile = UserProfile.objects.get(user=request.user)
            if not user_profile.stripe_customer_id:
                # Create Stripe customer if ID doesn't exist
                customer = stripe.Customer.create(
                    email=request.user.email,
                    name=f"{request.user.first_name} {request.user.last_name}",
                    metadata={
                        'user_id': request.user.id
                    }
                )
                user_profile.stripe_customer_id = customer.id
                user_profile.save()
            customer_id = user_profile.stripe_customer_id
        except UserProfile.DoesNotExist:
            # This shouldn't happen because of signals, but just in case
            raise Exception("User profile not found. Please contact support.")

        # Calculate credits
        credit_result = CreditCalculator.calculate_credits(amount, currency)

        # Create payment intent
        intent = stripe.PaymentIntent.create(
            customer=customer_id,  # Use the customer ID here
            payment_method=payment_method_id,
            amount=int(amount * 100),
            currency=currency.lower(),
            metadata={
                'user_id': request.user.id,
                'base_credits': credit_result.base_credits,
                'bonus_credits': credit_result.bonus_credits,
                'total_credits': credit_result.total_credits,
                'currency': currency
            },
            confirmation_method='manual',
            confirm=True,
            return_url=request.build_absolute_uri(reverse('credits:payment_success'))
        )

        if intent.status == 'succeeded':
            user_profile = UserProfile.objects.get(user=request.user)
            
            # Create a PaymentIntent first
            payment = stripe.PaymentIntent.retrieve(intent.id)
            
            # Create invoice using the same currency as the payment
            invoice = stripe.Invoice.create(
                customer=user_profile.stripe_customer_id,
                auto_advance=False,
                collection_method='charge_automatically',
                currency=currency.lower(),  # Explicitly set invoice currency
                pending_invoice_items_behavior='include',
                metadata={
                    'payment_intent_id': intent.id,
                }
            )

            # Create invoice item with matching currency
            stripe.InvoiceItem.create(
                customer=user_profile.stripe_customer_id,
                invoice=invoice.id,
                amount=payment.amount,
                currency=currency.lower(),  # Make sure currency matches
                description=f"Purchase of {credit_result.total_credits} credits ({credit_result.base_credits} base + {credit_result.bonus_credits} bonus)"
            )

            # Finalize and pay invoice
            finalized_invoice = stripe.Invoice.finalize_invoice(invoice.id)
            paid_invoice = stripe.Invoice.pay(invoice.id, paid_out_of_band=True)
            
            # Add credits and create transaction record
            add_credits_to_user(request.user, credit_result.total_credits)
            
            transaction = CreditTransaction.objects.create(
                user=request.user,
                amount=credit_result.total_credits,
                transaction_type='PURCHASE',
                payment_intent_id=intent.id,
                currency=currency,
                description=f"Purchased {credit_result.base_credits} credits + {credit_result.bonus_credits} bonus credits",
                stripe_invoice_id=paid_invoice.id,
                invoice_url=paid_invoice.hosted_invoice_url
            )

            return JsonResponse({
                'success': True,
                'redirect_url': reverse('credits:payment_success_with_id', kwargs={'transaction_id': transaction.id})
            })

        elif intent.status == 'requires_action':
            # 3D Secure authentication needed
            return JsonResponse({
                'requires_action': True,
                'payment_intent_client_secret': intent.client_secret
            })
            
        elif intent.status == 'requires_payment_method':
            # The payment failed - request new payment method
            return JsonResponse({
                'success': False,
                'error': 'Your card was declined. Please try a different payment method.'
            })
            
        elif intent.status == 'processing':
            # Payment is still processing
            return JsonResponse({
                'success': False,
                'error': 'Payment is processing. Please wait a moment and refresh the page.'
            })
            
        else:
            # Handle other states (canceled, failed)
            return JsonResponse({
                'success': False,
                'error': f'Payment {intent.status}. Please try again.'
            })

    except stripe.error.CardError as e:
        return JsonResponse({
            'success': False,
            'error': e.error.message
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        })

@login_required
def payment_success_general(request):
    return render(request, 'payment_success.html', {
        'success_message': 'Payment completed successfully!'
    })

@login_required
def payment_success(request, transaction_id=None):
    context = {}
    if transaction_id:
        try:
            transaction = CreditTransaction.objects.get(
                id=transaction_id,
                user=request.user
            )
            context['payment'] = {
                'amount': transaction.amount,
                'currency': transaction.currency,
                'credits_amount': transaction.amount,
                'invoice_url': transaction.invoice_url
            }
        except CreditTransaction.DoesNotExist:
            pass
    
    return render(request, 'payment_success.html', context)

@login_required
def credit_balance(request):
    user_credit, created = UserCredit.objects.get_or_create(user=request.user)
    transactions = CreditTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    return render(request, 'balance.html', {
        'balance': user_credit.balance,
        'transactions': transactions
    })

@login_required
def transaction_history(request):
    transactions = CreditTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    return render(request, 'transaction_history.html', {
        'transactions': transactions
    })