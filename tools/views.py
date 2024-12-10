from django.shortcuts import render
from django.http import JsonResponse
import random
from datetime import timedelta
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import logging
from .cover_letter import (
    generate_cover_letter_from_fields,

    generate_cover_letter_from_raw_text
)
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
    # Credit costs
    CREDIT_COSTS = {
        'manual_resume': 5,
        'upload_resume': 10,
        'manual_job': 3,
        'automated_job': 7
    }

    if request.method == "GET":
        context = {
            'page_title': 'Cover Letter AI',
            'page_description': 'Generate a professional cover letter using AI',
            'meta_description': 'Create a customized cover letter instantly with our AI-powered tool.',
            'manual_credit_cost': CREDIT_COSTS['manual_resume'],
            'automated_credit_cost': CREDIT_COSTS['upload_resume'],
            'manual_job_credit_cost': CREDIT_COSTS['manual_job'],
            'automated_job_credit_cost': CREDIT_COSTS['automated_job'],
        }
        return render(request, 'tools/cover_letter_generator.html', context)
    
    try:
        data = request.POST
        input_method = data.get('input_method')
        job_input_method = data.get('job_input_method')

        # Calculate total credits needed
        total_credits = (CREDIT_COSTS['upload_resume'] if input_method == 'upload' else CREDIT_COSTS['manual_resume']) + \
                       (CREDIT_COSTS['automated_job'] if job_input_method == 'unstructured' else CREDIT_COSTS['manual_job'])

        # TODO: Check if user has enough credits
        # if not user.has_enough_credits(total_credits):
        #     return JsonResponse({'success': False, 'error': 'Insufficient credits'}, status=402)

        # Handle resume input
        if input_method == 'manual':
            candidate_details = {
                'full_name': data.get('full_name'),
                'current_role': data.get('current_role'),
                'experience': data.get('experience'),
                'key_skills': data.get('key_skills'),
                'achievements': data.get('achievements')
            }
            resume_text = f"""
            {candidate_details['full_name']}
            {candidate_details['current_role']}

            Experience:
            {candidate_details['experience']}

            Achievements:
            {candidate_details['achievements']}

            Skills:
            {candidate_details['key_skills']}
            """
        else:  # upload
            resume_file = request.FILES.get('resume')
            if not resume_file:
                return JsonResponse({'success': False, 'error': 'Resume file is required.'}, status=400)
            resume_text = resume_file.read().decode('utf-8')

        # Handle job input
        if job_input_method == 'structured':
            job_details = {
                'position': data.get('position'),
                'company': data.get('company'),
                'department': data.get('department'),
                'description': data.get('description')
            }
            job_text = f"""
            Position: {job_details['position']}
            Company: {job_details['company']}
            Department: {job_details['department']}
            
            Description:
            {job_details['description']}
            """
        else:  # unstructured
            job_text = data.get('job_posting')
            if not job_text:
                return JsonResponse({'success': False, 'error': 'Job posting is required.'}, status=400)

        # Generate cover letter based on input combination
        if input_method == 'manual' and job_input_method == 'structured':
            result = generate_cover_letter_from_fields(job_details, candidate_details)
        else:
            result = generate_cover_letter_from_raw_text(job_text, resume_text)

        if result['success']:
            # TODO: Deduct credits from user's account
            # user.deduct_credits(total_credits)
            
            formatted_letter = result['cover_letter'].replace('\n', '<br>')
            return JsonResponse({
                'success': True,
                'cover_letter': formatted_letter,
                'credits_used': total_credits
            })
        else:
            return JsonResponse({
                'success': False,
                'error': result['error']
            }, status=500)

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
