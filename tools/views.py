from django.shortcuts import render
from django.http import JsonResponse
import random
from datetime import timedelta
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import logging
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie

from .cover_letter import (
    generate_cover_letter_from_fields,

    generate_cover_letter_from_raw_text
)
# Set up logging
logger = logging.getLogger(__name__)
@csrf_exempt  # Temporarily disable CSRF for testing
def visa_checker(request):
    # Debug prints
   
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
    # Sample school data (move this outside the function or to a separate file)
    sample_schools = {
        'usa': [
            {
                'name': 'Harvard University',
                'location': 'Cambridge, USA',
                'logo': 'path/to/harvard-logo.png',
                'tuition': 51925,  # Stored as number for easier filtering
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'work_opportunities': True,
                'housing_available': True,
                'website': 'https://www.harvard.edu',
                'fields_of_study': ['Business', 'Law', 'Medicine', 'Engineering'],
                'ranking': '#1 in USA'
            },
            {
                'name': 'MIT',
                'location': 'Massachusetts, USA',
                'logo': 'path/to/mit-logo.png',
                'tuition': '$53,790',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.mit.edu',
                'fields_of_study': ['Engineering', 'Computer Science', 'Business'],
                'ranking': '#2 in USA'
            },

        ],
        'uk': [
            {
                'name': 'University of Oxford',
                'location': 'Oxford, UK',
                'logo': 'path/to/oxford-logo.png',
                'tuition': '£26,770',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.ox.ac.uk',
                'fields_of_study': ['Arts', 'Sciences', 'Medicine'],
                'ranking': '#1 in UK'
            },
            {
                'name': 'University of Cambridge',
                'location': 'Cambridge, UK',
                'logo': 'path/to/cambridge-logo.png',
                'tuition': '£27,426',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.cam.ac.uk',
                'fields_of_study': ['Engineering', 'Business', 'Law'],
                'ranking': '#2 in UK'
            },
        ],
         'canada': [
            {
                'name': 'University of Toronto',
                'location': 'Toronto, Canada',
                'logo': 'path/to/uoft-logo.png',
                'tuition': 'CAD 45,900',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.utoronto.ca',
                'fields_of_study': ['Arts', 'Science', 'Medicine'],
                'ranking': '#1 in Canada'
            },
            {
                'name': 'McGill University',
                'location': 'Montreal, Canada',
                'logo': 'path/to/mcgill-logo.png',
                'tuition': 'CAD 45,500',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.mcgill.ca',
                'fields_of_study': ['Engineering', 'Medicine', 'Business'],
                'ranking': '#2 in Canada'
            },
        ],
        'australia': [
            {
                'name': 'University of Melbourne',
                'location': 'Melbourne, Australia',
                'logo': 'path/to/unimelb-logo.png',
                'tuition': 'AUD 45,000',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.unimelb.edu.au',
                'fields_of_study': ['Arts', 'Science', 'Engineering'],
                'ranking': '#1 in Australia'
            },
            {
                'name': 'University of Sydney',
                'location': 'Sydney, Australia',
                'logo': 'path/to/usyd-logo.png',
                'tuition': 'AUD 46,000',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.sydney.edu.au',
                'fields_of_study': ['Medicine', 'Business', 'Law'],
                'ranking': '#2 in Australia'
            },
        ],
        'germany': [
            {
                'name': 'Technical University of Munich',
                'location': 'Munich, Germany',
                'logo': 'path/to/tum-logo.png',
                'tuition': '€0 (Public University)',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.tum.de',
                'fields_of_study': ['Engineering', 'Computer Science', 'Medicine'],
                'ranking': '#1 in Germany'
            },
            {
                'name': 'Ludwig Maximilian University',
                'location': 'Munich, Germany',
                'logo': 'path/to/lmu-logo.png',
                'tuition': '€0 (Public University)',
                'programs': ['Undergraduate', 'Graduate', 'PhD'],
                'scholarships_available': True,
                'website': 'https://www.lmu.de',
                'fields_of_study': ['Arts', 'Sciences', 'Business'],
                'ranking': '#2 in Germany'
            },
        ]
    }

    if request.method == 'POST':
        # Get all filter parameters
        filters = {
            'country': request.POST.get('country', ''),
            'program_level': request.POST.get('program_level', ''),
            'field_of_study': request.POST.get('field_of_study', ''),
            'tuition_range': request.POST.get('tuition_range', ''),
            'scholarships_available': request.POST.get('scholarships_available') == 'true',
            'work_opportunities': request.POST.get('work_opportunities') == 'true',
            'housing_available': request.POST.get('housing_available') == 'true'
        }

        # Get schools for selected country
        schools = sample_schools.get(filters['country'].lower(), [])

        # Apply filters
        filtered_schools = []
        for school in schools:
            # Check program level
            if filters['program_level'] and filters['program_level'] not in [p.lower() for p in school['programs']]:
                continue

            # Check field of study
            if filters['field_of_study'] and filters['field_of_study'] not in [f.lower() for f in school['fields_of_study']]:
                continue

            # Check tuition range
            if filters['tuition_range']:
                tuition = school['tuition']
                range_min, range_max = map(int, filters['tuition_range'].split('-')) if '-' in filters['tuition_range'] else (30000, float('inf'))
                if not (range_min <= tuition <= range_max):
                    continue

            # Check additional filters
            if filters['scholarships_available'] and not school['scholarships_available']:
                continue
            if filters['work_opportunities'] and not school['work_opportunities']:
                continue
            if filters['housing_available'] and not school['housing_available']:
                continue

            filtered_schools.append(school)

        if not filtered_schools:
            return JsonResponse({
                'status': 'no_results',
                'message': 'No schools found matching your criteria.',
                'schools': []
            })

        return JsonResponse({
            'status': 'success',
            'message': f'Found {len(filtered_schools)} schools matching your criteria.',
            'schools': filtered_schools
        })

    # GET request - render initial page
    context = {
        'page_title': 'School Finder',
        'page_description': 'Find the perfect school matching your preferences, budget, and academic goals.',
        'filters': {
            'countries': list(sample_schools.keys()),
            'program_levels': [
                {'value': 'undergraduate', 'label': 'Undergraduate'},
                {'value': 'graduate', 'label': 'Graduate'},
                {'value': 'masters', 'label': 'Masters'},
                {'value': 'phd', 'label': 'PhD'}
            ],
            'fields_of_study': [
                {'value': 'business', 'label': 'Business'},
                {'value': 'engineering', 'label': 'Engineering'},
                {'value': 'medicine', 'label': 'Medicine'},
                {'value': 'law', 'label': 'Law'},
                {'value': 'computer_science', 'label': 'Computer Science'},
                {'value': 'arts', 'label': 'Arts'},
                {'value': 'sciences', 'label': 'Sciences'},
                {'value': 'architecture', 'label': 'Architecture'}
            ],
            'tuition_ranges': [
                {'value': '0-10000', 'label': '$0 - $10,000'},
                {'value': '10000-20000', 'label': '$10,000 - $20,000'},
                {'value': '20000-30000', 'label': '$20,000 - $30,000'},
                {'value': '30000-plus', 'label': '$30,000+'}
            ],
            'additional_filters': [
                {'id': 'scholarships_available', 'label': 'Scholarships Available'},
                {'id': 'work_opportunities', 'label': 'Work Opportunities'},
                {'id': 'housing_available', 'label': 'Housing Available'}
            ]
        }
    }
    
    return render(request, 'tools/school_finder.html', context)

import json
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import openai
import os
from openai import OpenAI

@require_http_methods(["GET", "POST"])
def job_cover_letter(request):
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
        return render(request, 'tools/job_cover_letter.html', context)
    
    try:
        data = request.POST
        input_method = data.get('input_method')
        job_input_method = data.get('job_input_method')

        # Calculate total credits needed
        total_credits = (CREDIT_COSTS['upload_resume'] if input_method == 'upload' else CREDIT_COSTS['manual_resume']) + \
                       (CREDIT_COSTS['automated_job'] if job_input_method == 'unstructured' else CREDIT_COSTS['manual_job'])

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
            
            # Get file extension
            file_extension = resume_file.name.split('.')[-1].lower()
            
            if file_extension == 'pdf':
                try:
                    import pdfplumber
                    with pdfplumber.open(resume_file) as pdf:
                        resume_text = ""
                        for page in pdf.pages:
                            resume_text += page.extract_text() or ""
                except ImportError:
                    return JsonResponse({
                        'success': False,
                        'error': 'PDF processing is not available. Please upload a TXT file.'
                    }, status=400)
                except Exception as e:
                    return JsonResponse({
                        'success': False,
                        'error': f'Error processing PDF file: {str(e)}'
                    }, status=400)
            elif file_extension == 'txt':
                try:
                    resume_text = resume_file.read().decode('utf-8')
                except UnicodeDecodeError:
                    try:
                        # Fallback to latin-1 if utf-8 fails
                        resume_text = resume_file.read().decode('latin-1')
                    except Exception as e:
                        return JsonResponse({
                            'success': False,
                            'error': f'Error reading text file: {str(e)}'
                        }, status=400)
            else:
                return JsonResponse({
                    'success': False,
                    'error': 'Unsupported file format. Please upload a PDF or TXT file.'
                }, status=400)

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

def visa_cover_letter(request):
    context = {
        'page_title': 'Visa Application Cover Letter',
        'page_description': 'Generate a visa application cover letter tailored to your needs.',
        'visa_credit_cost': 10,  # Example credit cost
    }
    return render(request, 'tools/visa_cover_letter.html', context)

def study_abroad_cover_letter(request):
    context = {
        'page_title': 'Study Abroad Cover Letter',
        'page_description': 'Create a study abroad cover letter for your university application.',
        'study_abroad_credit_cost': 8,  # Example credit cost
    }
    return render(request, 'tools/study_abroad_cover_letter.html', context)

def travel_sponsorship_cover_letter(request):
    context = {
        'page_title': 'Travel Sponsorship Cover Letter',
        'page_description': 'Draft a cover letter for travel sponsorship requests.',
        'sponsorship_credit_cost': 12,  # Example credit cost
    }
    return render(request, 'tools/travel_sponsorship_cover_letter.html', context)

def immigration_support_cover_letter(request):
    context = {
        'page_title': 'Immigration Support Letter',
        'page_description': 'Generate an immigration support letter for your application.',
        'immigration_credit_cost': 15,  # Example credit cost
    }
    return render(request, 'tools/immigration_support_cover_letter.html', context)

def tourist_invitation_cover_letter(request):
    context = {
        'page_title': 'Tourist Invitation Letter',
        'page_description': 'Create a tourist invitation letter for your guests.',
        'invitation_credit_cost': 5,  # Example credit cost
    }
    return render(request, 'tools/tourist_invitation_cover_letter.html', context)

def cover_letters(request):
    context = {
        'page_title': 'Cover Letter Generator',
        'page_description': 'Choose from our selection of professional cover letter templates',
        'job_credit_cost': 5,
        'visa_credit_cost': 10,
        'study_abroad_credit_cost': 8,
        'sponsorship_credit_cost': 12,
        'immigration_credit_cost': 15,
        'invitation_credit_cost': 5,
    }
    return render(request, 'tools/cover_letters.html', context)

def test_openai(request):
    try:
        # Get the API key
        api_key = os.getenv('OPENAI_API_KEY')
        
        # Check if key exists
        if not api_key:
            return JsonResponse({
                'status': 'error',
                'message': 'API key not found in environment'
            })
            
        # Try to initialize OpenAI client
        client = OpenAI()
        
        # Try a simple API call
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": "Hello"}],
            max_tokens=5
        )
        
        return JsonResponse({
            'status': 'success',
            'message': 'OpenAI API is working',
            'response': response.choices[0].message.content
        })
        
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': f'Error testing OpenAI: {str(e)}'
        })

def all_tools(request):
    return render(request, 'tools/all-tools.html')
 