from django.shortcuts import render
from django.http import JsonResponse
from .services.email_service import EmailManager
from django.views.decorators.http import require_http_methods
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import json
import os
from dotenv import load_dotenv
import logging
from .models import WhatsAppConversation, WhatsAppMessage

# Load environment variables
load_dotenv()
logger = logging.getLogger(__name__)

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
    



 
@csrf_exempt
@require_http_methods(["GET", "POST"])
def whatsapp_webhook(request):
    if request.method == 'GET':
        # Handle WhatsApp verification
        verify_token = os.getenv('WHATSAPP_VERIFY_TOKEN')
        mode = request.GET.get('hub.mode')
        token = request.GET.get('hub.verify_token')
        challenge = request.GET.get('hub.challenge')
        
        # Log verification attempt
        logger.info(f"Webhook verification attempt - Mode: {mode}, Token: {token}, Challenge: {challenge}")
        
        if mode and token:
            if mode == 'subscribe' and token == verify_token:
                # Convert challenge to integer and return
                try:
                    challenge_int = int(challenge)
                    logger.info(f"Webhook verified successfully with challenge: {challenge_int}")
                    return HttpResponse(challenge_int)
                except (ValueError, TypeError) as e:
                    logger.error(f"Invalid challenge value: {challenge}. Error: {str(e)}")
                    return HttpResponse('Invalid challenge value', status=400)
            else:
                logger.warning("Invalid verification token or mode")
                return HttpResponse('Invalid verification token', status=403)
        else:
            logger.warning("Missing verification parameters")
            return HttpResponse('Missing parameters', status=400)
        
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            logger.info(f"Received WhatsApp webhook: {data}")
            
            # Extract message data
            entry = data['entry'][0]
            changes = entry['changes'][0]
            value = changes['value']
            message = value['messages'][0]
            
            # Get or create conversation
            conversation, created = WhatsAppConversation.objects.get_or_create(
                customer_id=message['from'],
                defaults={
                    'customer_phone': message['from'],
                    'status': 'active'
                }
            )
            
            # Save message
            WhatsAppMessage.objects.create(
                conversation=conversation,
                message_id=message['id'],
                direction='incoming',
                content=message.get('text', {}).get('body', ''),
                media_url=message.get('media', {}).get('url', ''),
                media_type=message.get('type', 'text'),
                status='received'
            )
            
            logger.info(f"Saved WhatsApp message from {message['from']}")
            return HttpResponse('OK')
            
        except KeyError as e:
            logger.error(f"Invalid webhook data structure: {str(e)}")
            return HttpResponse('Invalid webhook data', status=400)
        except Exception as e:
            logger.error(f"Error processing WhatsApp webhook: {str(e)}")
            return HttpResponse('Error processing webhook', status=500)   