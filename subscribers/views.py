from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
from .forms import SubscriberForm
from .models import Subscriber

# Create your views here.


@require_POST
@csrf_exempt  # Add this decorator

def subscribe(request):
    # Debug prints
    print("POST data received:", request.POST)
    print("Subscription type from POST:", request.POST.get('subscription_type'))
    
    # Get the subscription type from POST data without a default
    subscription_type = request.POST.get('subscription_type')
    
    # Validate subscription type
    if subscription_type not in dict(Subscriber.SUBSCRIPTION_TYPES):
        return JsonResponse({
            'status': 'error',
            'message': 'Invalid subscription type'
        }, status=400)
    
    # Create form with both email and subscription_type
    form_data = {
        'email': request.POST.get('email'),
        'subscription_type': subscription_type
    }
    print("Form data being used:", form_data)
    
    form = SubscriberForm(form_data)
    
    if form.is_valid():
        print("Form is valid. About to save with data:", form.cleaned_data)
        try:
            subscriber = form.save()
            print("Subscriber saved with type:", subscriber.subscription_type)
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for subscribing!'
            })
        except Exception as e:
            print("Error saving subscriber:", str(e))
            if 'unique constraint' in str(e).lower():
                return JsonResponse({
                    'status': 'error',
                    'message': 'You are already subscribed!'
                }, status=400)
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again.'
            }, status=400)
    else:
        print("Form errors:", form.errors)
        return JsonResponse({
            'status': 'error',
            'message': 'Please enter a valid email address.'
        }, status=400)
