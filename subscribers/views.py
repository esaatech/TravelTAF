from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_protect
from .forms import SubscriberForm

# Create your views here.

@require_POST
@csrf_protect
def subscribe(request):
    form = SubscriberForm(request.POST)
    if form.is_valid():
        try:
            form.save()
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for subscribing!'
            })
        except Exception as e:
            if 'unique constraint' in str(e).lower():
                return JsonResponse({
                    'status': 'error',
                    'message': 'You are already subscribed!'
                }, status=400)
            return JsonResponse({
                'status': 'error',
                'message': 'An error occurred. Please try again.'
            }, status=400)
    return JsonResponse({
        'status': 'error',
        'message': 'Please enter a valid email address.'
    }, status=400)
