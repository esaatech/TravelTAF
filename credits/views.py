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
stripe.api_key = settings.STRIPE_SECRET_KEY

@login_required
def purchase_credits(request):
    return render(request, 'purchase.html', {
        'STRIPE_PUBLIC_KEY': settings.STRIPE_PUBLIC_KEY
    })

@login_required
@require_POST
@csrf_protect
def process_payment(request):
    try:
        data = json.loads(request.body)
        payment_method_id = data.get('payment_method_id')
        amount = float(data.get('amount'))
        currency = data.get('currency', 'USD')  # Default to USD if not specified

        # Calculate credits
        credit_result = CreditCalculator.calculate_credits(amount, currency)

        # Create payment intent with metadata
        intent = stripe.PaymentIntent.create(
            payment_method=payment_method_id,
            amount=int(amount * 100),  # Convert to cents
            currency=currency.lower(),
            metadata={
                'user_id': request.user.id,
                'base_credits': credit_result.base_credits,
                'bonus_credits': credit_result.bonus_credits,
                'total_credits': credit_result.total_credits,
                'currency': currency
            },
            confirmation_method='manual',
            confirm=True
        )

        if intent.status == 'succeeded':
            # Add credits to user account
            add_credits_to_user(request.user, credit_result.total_credits)
            
            # Create transaction record
            CreditTransaction.objects.create(
                user=request.user,
                amount=credit_result.total_credits,
                transaction_type='PURCHASE',
                payment_intent_id=intent.id,
                currency=currency,
                description=f"Purchased {credit_result.base_credits} credits + {credit_result.bonus_credits} bonus credits"
            )

            return JsonResponse({
                'success': True,
                'redirect_url': reverse('credits:payment_success')
            })
        else:
            return JsonResponse({
                'success': False,
                'error': 'Payment failed'
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
def payment_success(request, payment_id):
    payment = get_object_or_404(CreditPayment, id=payment_id, user=request.user)
    
    if payment.status == 'confirmed' and not payment.extra_data.get('credits_added'):
        # Calculate credits from the payment amount
        credits_to_add = payment.total  # Or use your CreditCalculator here
        
        # Add credits to user
        add_credits_to_user(request.user, credits_to_add)
        
        # Mark credits as added to prevent double-crediting
        payment.extra_data = {'credits_added': True}
        payment.save()
        
        messages.success(request, f'{credits_to_add} credits have been added to your account!')
    
    return render(request, 'credits/payment_success.html', {
        'payment': payment
    })

@login_required
def credit_balance(request):
    user_credit, created = UserCredit.objects.get_or_create(user=request.user)
    transactions = CreditTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    return render(request, 'balance.html', {
        'balance': user_credit.balance,
        'transactions': transactions
    })
