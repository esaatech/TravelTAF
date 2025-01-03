from django.shortcuts import render
from django.http import JsonResponse
from .services.email_service import EmailManager
from django.views.decorators.http import require_http_methods
import json

# Create your views here.

def submit_study_abroad_form(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        # Convert target_countries from string to list if needed
        form_data['target_countries'] = request.POST.getlist('target_countries[]')
        
        # Send emails
        success, message = EmailManager.send_form_submission_email(
            form_data,
            'study_abroad'
        )
        
        if success:
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your submission. We will contact you soon!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'There was an error processing your request. Please try again.'
            }, status=400)
    else:
        return render(request, 'services/study_abroad.html')

def submit_moving_abroad_form(request):
    if request.method == 'POST':
        form_data = request.POST.dict()
        form_data['target_countries'] = request.POST.getlist('target_countries[]')
        
        success, message = EmailManager.send_form_submission_email(
            form_data,
            'moving_abroad'
        )
        
        if success:
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your submission. We will contact you soon!'
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'There was an error processing your request. Please try again.'
            }, status=400)
    else:
        return render(request, 'services/moving_abroad.html')

@require_http_methods(["POST"])
def register_user(request):
    try:
        data = json.loads(request.body)
        
        # Send welcome email
        email_manager = EmailManager()
        success, message = email_manager.send_welcome_email({
            'email': data.get('email'),
            'full_name': data.get('full_name')
        })
        
        if not success:
            print(f"Warning: Welcome email failed - {message}")
            
        return JsonResponse({
            'status': 'success',
            'message': 'Registration successful'
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)