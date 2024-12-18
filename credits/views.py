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
        amount = int(float(data.get('amount')) * 100)  # Convert to cents

        # Create payment intent
        intent = stripe.PaymentIntent.create(
            payment_method=payment_method_id,
            amount=amount,
            currency='usd',
            confirmation_method='manual',
            confirm=True,
            metadata={
                'user_id': request.user.id,
                'credits': calculate_credits(amount/100)  # Add your credit calculation logic
            }
        )

        if intent.status == 'succeeded':
            # Create payment record and add credits
            payment = CreditPayment.objects.create(
                user=request.user,
                amount=amount/100,
                payment_id=intent.id
            )
            
            add_credits_to_user(request.user, amount/100)

            return JsonResponse({
                'success': True,
                'redirect_url': reverse('credits:payment_success', args=[payment.id])
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
    payment = get_object_or_404(CreditPayment, id=payment_id)
    
    if payment.status == PaymentStatus.CONFIRMED:
        with transaction.atomic():
            user_credit, created = UserCredit.objects.get_or_create(user=request.user)
            user_credit.balance += payment.total
            user_credit.save()

            CreditTransaction.objects.create(
                user=request.user,
                amount=payment.total,
                transaction_type='PURCHASE',
                payment=payment,
                description=f"Credit purchase of {payment.total}"
            )

        messages.success(request, f'Successfully added {payment.total} credits to your account!')
    
    return redirect('credits:balance')

@login_required
def credit_balance(request):
    user_credit, created = UserCredit.objects.get_or_create(user=request.user)
    transactions = CreditTransaction.objects.filter(user=request.user).order_by('-created_at')[:10]
    
    return render(request, 'balance.html', {
        'balance': user_credit.balance,
        'transactions': transactions
    })
