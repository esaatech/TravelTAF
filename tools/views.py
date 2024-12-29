from django.shortcuts import render
from django.http import JsonResponse
import random
from datetime import timedelta
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import logging
from django.views.decorators.csrf import ensure_csrf_cookie
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from asgiref.sync import sync_to_async
import asyncio
from .models import School, Country, ProgramLevel, FieldOfStudy
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import os
from openai import OpenAI
from .services.amadeus import AmadeusFlightService
from .services.flight_interfaces import FlightSearchParams, FlightDestination

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
        search_type = request.POST.get('searchType', 'specific')
        
        if not from_country:
            return JsonResponse({
                'error': 'Nationality is required'
            }, status=400)

        # Handle different search types
        if search_type == 'specific':
            to_country = request.POST.get('toCountry')
            if not to_country:
                return JsonResponse({
                    'error': 'Destination country is required for specific search'
                }, status=400)

            # Your existing specific country logic
            visa_statuses = ['visa_required', 'visa_free', 'visa_on_arrival', 'e_visa']
            processing_times = ['5-7 business days', '10-15 business days', '3-4 weeks', '24-48 hours']
            costs = ['$50', '$100', '$150', '$200', 'Free']
            
            response_data = {
                'searchType': 'specific',
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
        
        else:
            # Handle visa_free or eta searches
            # For testing, return random countries
            sample_countries = [
                {'name': 'Canada', 'code': 'CA'},
                {'name': 'Japan', 'code': 'JP'},
                {'name': 'Singapore', 'code': 'SG'},
                {'name': 'United Kingdom', 'code': 'GB'},
                {'name': 'Australia', 'code': 'AU'},
                {'name': 'New Zealand', 'code': 'NZ'}
            ]
            
            # Randomly select 3-5 countries for demonstration
            selected_countries = random.sample(sample_countries, random.randint(3, 5))
            
            response_data = {
                'searchType': search_type,
                'countries': selected_countries
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

def resume_builder(request):
    return render(request, 'tools/resume_builder.html')

def resume_review(request):
    return render(request, 'tools/resume_review.html')

def language_test(request):
    return render(request, 'tools/language_test.html')

def job_search(request):
    context = {
        'page_title': 'International Job Search Resources',
        'page_description': 'Access curated job boards and premium tools to find international job opportunities and optimize your applications.',
        'resume_services': {
            'builder_cost': 25,  # Combined cost for build & optimize
            'cover_letter_cost': 15,  # Cost for cover letter
        },
        'countries': {
            'usa': {
                'name': 'United States',
                'job_boards': [
                    {
                        'name': 'LinkedIn Jobs',
                        'url': 'https://www.linkedin.com/jobs',
                        'description': 'Professional networking and job search platform with extensive US listings.'
                    },
                    {
                        'name': 'H1B.io',
                        'url': 'https://h1b.io/',
                        'description': 'Specialized in H1B visa sponsorship jobs.'
                    },
                    {
                        'name': 'MyVisaJobs',
                        'url': 'https://www.myvisajobs.com/',
                        'description': 'Focus on visa-sponsored jobs and H1B opportunities.'
                    }
                ],
                'visa_info': 'Most common work visas: H1B, L1, O1',
                'avg_salary': '$65,000 - $120,000'
            },
            'canada': {
                'name': 'Canada',
                'job_boards': [
                    {
                        'name': 'Job Bank Canada',
                        'url': 'https://www.jobbank.gc.ca/',
                        'description': 'Official Canadian government job site.'
                    },
                    {
                        'name': 'Indeed Canada',
                        'url': 'https://ca.indeed.com/',
                        'description': 'Large job aggregator with Canadian opportunities.'
                    }
                ],
                'visa_info': 'Work permits via LMIA or Express Entry',
                'avg_salary': 'CAD 55,000 - 95,000'
            },
            # Add more countries...
        }
    }
    return render(request, 'tools/job_search.html', context)

def school_finder(request):
    """
    Handle school finder page and search functionality
    """
    if request.method == 'POST':
        # Get filter parameters
        country_code = request.POST.get('country', '')
        program_level = request.POST.get('program_level', '')
        field_of_study = request.POST.get('field_of_study', '')
        tuition_range = request.POST.get('tuition_range', '')
        
        # Additional filters
        scholarships = request.POST.get('scholarships_available') == 'true'
        work_opportunities = request.POST.get('work_opportunities') == 'true'
        housing_available = request.POST.get('housing_available') == 'true'
        
        # Get filtered schools
        filtered_schools = get_filtered_schools(
            country_code, program_level, field_of_study, 
            tuition_range, scholarships, work_opportunities, housing_available
        )
        
        # Return JSON response
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
            'countries': [
                {'value': country.code, 'label': country.name}
                for country in Country.objects.all()
            ],
            'program_levels': [
                {'value': program.value, 'label': program.name}
                for program in ProgramLevel.objects.all()
            ],
            'fields_of_study': [
                {'value': field.value, 'label': field.name}
                for field in FieldOfStudy.objects.all()
            ],
            'tuition_ranges': [
                {'value': 'free', 'label': 'Free Education'},
                {'value': '0-10000', 'label': '$1 - $10,000'},
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

def get_filtered_schools(country_code, program_level, field_of_study, tuition_range, 
                        scholarships=False, work_opportunities=False, housing_available=False):
    """
    Filter schools based on search criteria using database queries
    """
    # Start with all schools
    schools = School.objects.all()

    # Apply country filter
    if country_code:
        schools = schools.filter(country__code=country_code)

    # Apply program level filter
    if program_level:
        schools = schools.filter(programs__value=program_level)

    # Apply field of study filter
    if field_of_study:
        schools = schools.filter(fields_of_study__value=field_of_study)

    # Apply tuition range filter
    if tuition_range:
        if tuition_range == 'free':
            schools = schools.filter(tuition=0)
        elif tuition_range == '30000-plus':
            schools = schools.filter(tuition__gte=30000)
        else:
            try:
                min_tuition, max_tuition = map(int, tuition_range.split('-'))
                schools = schools.filter(tuition__gte=min_tuition, tuition__lte=max_tuition)
            except ValueError:
                pass

    # Apply additional filters
    if scholarships:
        schools = schools.filter(scholarships_available=True)
    if work_opportunities:
        schools = schools.filter(work_opportunities=True)
    if housing_available:
        schools = schools.filter(housing_available=True)

    # Convert queryset to list of dictionaries
    return [
        {
            'id': school.id,
            'name': school.name,
            'location': school.location,
            'logo': school.logo.url if school.logo else None,
            'tuition': float(school.tuition),
            'programs': [p.name for p in school.programs.all()],
            'scholarships_available': school.scholarships_available,
            'work_opportunities': school.work_opportunities,
            'housing_available': school.housing_available,
            'website': school.website,
            'fields_of_study': [f.name for f in school.fields_of_study.all()],
            'ranking': school.ranking
        }
        for school in schools.distinct()
    ]



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





def flight_search(request):
    if request.method == 'POST':
        try:
            service = AmadeusFlightService()
            params = FlightSearchParams(
                origin=request.POST.get('origin'),
                max_price=float(request.POST.get('maxPrice')) if request.POST.get('maxPrice') else None
            )
            
            results = asyncio.run(service.search_destinations(params))
            return JsonResponse({
                'success': True,
                'results': [vars(result) for result in results]
            }, safe=False)
            
        except Exception as e:
            print(f"Error: {str(e)}")  # Debug log
            return JsonResponse({
                'success': False,
                'error': str(e)
            })
    
    return render(request, 'tools/flight_search.html')

from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

class SchoolDetailView(DetailView):
    model = School
    template_name = 'tools/school_detail.html'
    context_object_name = 'school'
    pk_url_kwarg = 'school_id'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        school = self.get_object()

        # Get service plans
        context['service_plans'] = {
            'program_support': {
                'name': 'Program Application Support',
                'price': 199,
                'description': 'Complete support for applying to your chosen program',
                'features': [
                    'Document preparation assistance',
                    'Personal Statement/SOP writing',
                    'Application form filling guidance',
                    'Document review & verification',
                    'Application submission support',
                    'Interview preparation (if required)',
                    'Admission status tracking',
                    'Email templates for communication',
                ],
                'included_services': [
                    'One program application',
                    '3 rounds of document review',
                    '2 SOP/Essay revisions',
                    '1 mock interview session',
                ],
                'timeline': '4-6 weeks',
                'button_text': 'Start Application',
                'button_url': 'tools:start_program_application',
            },
            'study_abroad': {
                'name': 'Complete Study Abroad Service',
                'price': 999,
                'description': 'End-to-end support for your entire study abroad journey',
                'features': [
                    'All Program Application Support features',
                    'Multiple program applications',
                    'Visa application assistance',
                    'Pre-departure guidance',
                    'Accommodation search support',
                    'Bank account setup assistance',
                    'Travel insurance guidance',
                    'Airport pickup arrangement',
                ],
                'included_services': [
                    'Up to 3 program applications',
                    'Unlimited document reviews',
                    'Complete visa application support',
                    'Accommodation shortlisting',
                    '24/7 support until arrival',
                    '3-month post-arrival support',
                ],
                'timeline': '3-6 months',
                'button_text': 'Get Complete Support',
                'button_url': 'tools:start_abroad_service',
            }
        }

        # Application requirements and process
        context['requirements'] = {
            'documents': [
                {'name': 'Academic transcripts', 'required': True},
                {'name': 'Language test scores', 'required': True},
                {'name': 'Statement of purpose', 'required': True},
                {'name': 'Letters of recommendation', 'required': True},
                {'name': 'CV/Resume', 'required': False},
                {'name': 'Portfolio (if applicable)', 'required': False},
                {'name': 'Financial documents', 'required': True},
                {'name': 'Passport', 'required': True},
            ],
            'process_steps': [
                {
                    'phase': 'Initial Consultation',
                    'duration': '1 week',
                    'description': 'Review your profile and requirements, plan application strategy'
                },
                {
                    'phase': 'Document Preparation',
                    'duration': '2-3 weeks',
                    'description': 'Prepare and review all required documents'
                },
                {
                    'phase': 'Application Submission',
                    'duration': '1-2 weeks',
                    'description': 'Submit application and track status'
                },
                {
                    'phase': 'Post-Application Support',
                    'duration': 'Ongoing',
                    'description': 'Interview preparation and admission follow-up'
                },
            ]
        }

        return context