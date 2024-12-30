from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import SubscriptionPlan, PlanDuration, UserSubscription, UserProfile
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse
import stripe
import json
import os
from dotenv import load_dotenv
load_dotenv()
# Initialize Stripe with SECRET key (not publishable key)
stripe.api_key = os.getenv('STRIPE_SECRET_KEY')  # Make sure this is the secret key

class PlanPurchaseView(LoginRequiredMixin, DetailView):
    """
    Generic view to display any subscription plan details and handle purchase.
    Can be used by any app that needs subscription functionality.
    """
    template_name = 'subscriptions/purchase.html'
    model = SubscriptionPlan
    context_object_name = 'plan'
    pk_url_kwarg = 'plan_id'

    def get_queryset(self):
        """Ensure we only get active plans with their durations."""
        return SubscriptionPlan.objects.filter(
            is_active=True
        ).prefetch_related(
            'durations',
            'features'
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        plan = self.get_object()
        
        # Add plan ID to context
        context['plan_id'] = plan.id
        
        # Get active durations for this plan
        context['durations'] = plan.durations.filter(is_active=True)
        
        # Separate features into tools and services
        context['tools'] = plan.features.filter(
            type='TOOL',
            is_active=True
        )
        context['services'] = plan.features.filter(
            type='SERVICE',
            is_active=True
        )
        
        # Load Stripe publishable key directly
        context['STRIPE_PUBLIC_KEY'] = os.getenv('STRIPE_PUBLISHABLE_KEY')
        
        # Add return_url if provided
        context['return_url'] = self.request.GET.get('return_url')
        
        return context

@login_required
def process_payment(request, plan_id, duration_id):
    """Handle the payment processing and subscription creation."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    try:
        # Get data from request
        data = json.loads(request.body)
        payment_method_id = data.get('payment_method_id')
        save_card = data.get('save_card', False)
        return_url = data.get('return_url')

        # Get or create stripe profile
        stripe_profile, created = UserProfile.objects.get_or_create(user=request.user)

        # Create or get Stripe customer
        if not stripe_profile.stripe_customer_id:
            customer = stripe.Customer.create(
                email=request.user.email,
                payment_method=payment_method_id if save_card else None,
                metadata={'user_id': request.user.id}
            )
            stripe_profile.stripe_customer_id = customer.id
            stripe_profile.save()
        else:
            customer = stripe.Customer.retrieve(stripe_profile.stripe_customer_id)
            if save_card:
                stripe.PaymentMethod.attach(payment_method_id, customer=customer.id)

        # Get plan and duration
        plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
        duration = get_object_or_404(
            PlanDuration, 
            id=duration_id, 
            plan=plan, 
            is_active=True
        )

        # Create pending subscription
        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            plan_duration=duration,
            status='PENDING'
        )

        # Create payment intent
        payment_intent = stripe.PaymentIntent.create(
            amount=int(duration.price * 100),  # Convert to cents
            currency='usd',
            customer=customer.id,
            payment_method=payment_method_id,
            off_session=False,
            confirm=True,
            metadata={
                'subscription_id': subscription.id,
                'plan_id': plan.id,
                'duration_id': duration.id
            }
        )

        # Handle the payment intent status
        if payment_intent.status == 'succeeded':
            subscription.status = 'ACTIVE'
            subscription.stripe_payment_intent = payment_intent.id
            subscription.save()

            success_url = return_url or reverse('subscriptions:checkout_success', 
                                              args=[subscription.id])
            
            return JsonResponse({
                'success': True,
                'redirect_url': success_url
            })
        else:
            subscription.delete()
            return JsonResponse({
                'success': False,
                'error': 'Payment failed'
            }, status=400)

    except stripe.error.CardError as e:
        # Handle card errors
        if 'subscription' in locals():
            subscription.delete()
        return JsonResponse({
            'success': False,
            'error': e.user_message
        }, status=400)

    except Exception as e:
        # Handle other errors
        if 'subscription' in locals():
            subscription.delete()
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)

@login_required
def checkout_success(request, subscription_id):
    """Generic success page for subscription checkout."""
    subscription = get_object_or_404(
        UserSubscription,
        id=subscription_id,
        user=request.user
    )
    return render(request, 'subscriptions/success.html', {
        'subscription': subscription
    })

# Create your views here.
