from django.shortcuts import render
from django.http import JsonResponse
import random
from datetime import timedelta
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
from .cover_letter import generate_cover_letter_from_fields, generate_cover_letter_from_raw_text
import logging

# Set up logging
logger = logging.getLogger(__name__)

def visa_checker(request):
    if request.method == 'POST':
        from_country = request.POST.get('fromCountry')
        to_country = request.POST.get('toCountry')
        
        if not from_country or not to_country:
            return JsonResponse({
                'error': 'Both countries are required'
            }, status=400)

        # Simulate API response
        visa_statuses = ['visa_required', 'visa_free', 'visa_on_arrival', 'e_visa']
        processing_times = ['5-7 business days', '10-15 business days', '3-4 weeks', '24-48 hours']
        costs = ['$50', '$100', '$150', '$200', 'Free']
        
        response_data = {
            'status': random.choice(visa_statuses),
            'details': {
                'processing_time': random.choice(processing_times),
                'validity': f"{random.randint(1, 12)} months",
                'cost': random.choice(costs),
                'max_stay': f"{random.randint(30, 180)} days",
                'entry_type': random.choice(['Single', 'Multiple']),
                'requirements': [
                    'Valid passport',
                    'Passport-size photos',
                    'Bank statements',
                    'Travel insurance',
                    'Hotel bookings',
                    'Return ticket'
                ],
                'additional_info': [
                    'Passport must be valid for at least 6 months',
                    'Must have at least 2 blank pages in passport',
                    'Proof of sufficient funds may be required'
                ]
            }
        }
        
        return JsonResponse(response_data)
        
    return render(request, 'tools/visa_checker.html')

def points_calculator(request):
    return render(request, 'tools/points_calculator.html')

def cost_estimator(request):
    return render(request, 'tools/cost_estimator.html')

def document_checker(request):
    return render(request, 'tools/document_checker.html')

def timeline_planner(request):
    return render(request, 'tools/timeline_planner.html')

def language_test(request):
    return render(request, 'tools/language_test.html')

def job_search(request):
    return render(request, 'tools/job_search.html')

def school_finder(request):
    return render(request, 'tools/school_finder.html')

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import openai

@require_http_methods(["GET", "POST"])
def generate_cover_letter(request):
    if request.method == "GET":
        context = {
            'page_title': 'Cover Letter AI',
            'page_description': 'Generate a professional cover letter using AI',
            'meta_description': 'Create a customized cover letter instantly with our AI-powered tool. Upload your resume and get a professionally written cover letter tailored to your job application.',
            'manual_credit_cost': 5,
            'automated_credit_cost': 10,
            'manual_job_credit_cost': 3,
            'automated_job_credit_cost': 7,
        }
        return render(request, 'tools/cover_letter_generator.html', context)
    
    # Handle POST request
    try:
        # Get form data
        data = request.POST
        input_method = data.get('input_method')
        job_input_method = data.get('job_input_method')

        # Validate input data
        if input_method == 'manual':
            candidate_details = {
                'name': data.get('full_name'),
                'current_role': data.get('current_role'),
                'experience': data.get('experience'),
                'skills': data.get('key_skills'),
                'achievements': data.get('achievements')
            }
            if not all(candidate_details.values()):
                return JsonResponse({'success': False, 'error': 'All candidate fields are required for manual input.'}, status=400)
        else:
            resume_text = request.FILES.get('resume')
            if not resume_text:
                return JsonResponse({'success': False, 'error': 'Resume file is required for automated extraction.'}, status=400)

        if job_input_method == 'structured':
            job_details = {
                'position': data.get('position'),
                'company': data.get('company'),
                'department': data.get('department'),
                'description': data.get('description')
            }
            if not all(job_details.values()):
                return JsonResponse({'success': False, 'error': 'All job fields are required for structured input.'}, status=400)
        else:
            job_posting = data.get('job_posting')
            if not job_posting:
                return JsonResponse({'success': False, 'error': 'Job posting is required for unstructured input.'}, status=400)

        # Generate cover letter
        if input_method == 'manual' and job_input_method == 'structured':
            cover_letter = generate_cover_letter_from_fields(job_details, candidate_details)
        else:
            cover_letter = generate_cover_letter_from_raw_text(job_posting, resume_text.read().decode('utf-8'))

        return JsonResponse({'success': True, 'cover_letter': cover_letter.replace('\n', '<br>')})

    except Exception as e:
        logger.error("Error generating cover letter", exc_info=True)
        return JsonResponse({'success': False, 'error': str(e)}, status=500)
