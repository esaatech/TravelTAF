from django.shortcuts import render
from django.http import JsonResponse
import random
from datetime import timedelta

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
        # Render the form template
        context = {
            'page_title': 'Cover Letter AI',
            'page_description': 'Generate a professional cover letter using AI',
            'meta_description': 'Create a customized cover letter instantly with our AI-powered tool. Upload your resume and get a professionally written cover letter tailored to your job application.',
        }
        return render(request, 'tools/cover_letter_generator.html', context)
    
    # Handle POST request (existing code)
    try:
        # Get form data
        data = request.POST
        
        # Construct the prompt for GPT
        prompt = f"""
        Generate a professional cover letter with the following details:

        Applicant Information:
        - Name: {data.get('full_name')}
        - Email: {data.get('email')}
        - Phone: {data.get('phone')}
        - Location: {data.get('location')}

        Job Details:
        - Company: {data.get('company_name')}
        - Position: {data.get('job_title')}
        - Job Description: {data.get('job_description')}

        Applicant's Key Skills:
        {data.get('key_skills')}

        Relevant Experience:
        {data.get('relevant_experience')}

        Please write a compelling cover letter that:
        1. Addresses the specific job requirements
        2. Highlights relevant skills and experience
        3. Shows enthusiasm for the role and company
        4. Maintains a professional yet engaging tone
        5. Includes proper formatting with date and contact information
        """

        # Call OpenAI API
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a professional cover letter writer."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=1000
        )

        # Get the generated cover letter
        cover_letter = response.choices[0].message.content

        # Format the cover letter with HTML
        formatted_letter = cover_letter.replace('\n', '<br>')

        return JsonResponse({
            'success': True,
            'cover_letter': formatted_letter
        })

    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=500)
