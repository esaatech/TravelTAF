from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.conf import settings
from .models import SubscriptionPlan, PlanDuration, UserSubscription
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.urls import reverse

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
        
        # Add Stripe public key
        context['STRIPE_PUBLIC_KEY'] = settings.STRIPE_PUBLIC_KEY
        
        # Add return_url if provided
        context['return_url'] = self.request.GET.get('return_url')
        
        return context

@login_required
def process_payment(request, plan_id, duration_id):
    """Handle the payment processing and subscription creation."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request method'}, status=400)

    plan = get_object_or_404(SubscriptionPlan, id=plan_id, is_active=True)
    duration = get_object_or_404(
        PlanDuration, 
        id=duration_id, 
        plan=plan, 
        is_active=True
    )

    try:
        # Create pending subscription first
        subscription = UserSubscription.objects.create(
            user=request.user,
            plan=plan,
            plan_duration=duration,
            status='PENDING'
        )

        # Process payment with Stripe
        # TODO: Add Stripe payment processing here
        
        # Get return URL from request if provided
        return_url = request.POST.get('return_url')
        
        if return_url:
            success_url = return_url
        else:
            success_url = reverse('subscriptions:checkout_success', 
                                args=[subscription.id])
        
        return JsonResponse({
            'success': True,
            'redirect_url': success_url
        })
    except Exception as e:
        # If anything fails, delete the subscription
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
