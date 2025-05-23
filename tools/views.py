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
from .models import School, Country, ProgramLevel, FieldOfStudy, StudyServicePlan, VisaRelationship, Countries
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_protect
import os
from openai import OpenAI
from .services.amadeus import AmadeusFlightService
from .services.flight_interfaces import FlightSearchParams, FlightDestination
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic import View
from subscriptions.models import SubscriptionPlan
from tools.models import VisaType

from .cover_letter import (
    generate_cover_letter_from_fields,

    generate_cover_letter_from_raw_text
)
# Set up logging
logger = logging.getLogger(__name__)
@csrf_exempt  # Temporarily disable CSRF for testing
def visa_checker(request):
    print("\n=== New Visa Checker Request ===")
    print(f"Method: {request.method}")
    print(f"POST params: {request.POST}")
    
    if request.method == 'POST':
        from_country = request.POST.get('fromCountry')
        to_country = request.POST.get('toCountry')
        search_type = request.POST.get('searchType')
        
        try:
            base_query = VisaRelationship.objects.select_related(
                'visa_type', 
                'citizenship_country', 
                'destination_country'
            ).filter(
                citizenship_country__iso_code_2=from_country,
                is_active=True
            )

            def format_visa_info(relationship):
                return {
                    'country_name': relationship.destination_country.name,
                    'country_code': relationship.destination_country.iso_code_2,
                    'visa_type': relationship.visa_type.name,
                    'max_stay': relationship.max_stay_days,
                    'multiple_entry': relationship.multiple_entry,
                    'processing_time': relationship.processing_time_days,
                    'fee': f"{relationship.fee_amount} {relationship.fee_currency}" if relationship.fee_amount else None,
                    'documents': relationship.documents_required,
                    'notes': relationship.notes,
                    'last_verified': relationship.last_verified_date.strftime('%Y-%m-%d') if relationship.last_verified_date else None,
                    'is_visa_free': relationship.is_visa_free,
                    'is_eta': relationship.is_eta
                }

            if search_type in ['visa_free', 'eta']:
                filter_params = {'is_visa_free': True} if search_type == 'visa_free' else {'is_eta': True}
                relationships = base_query.filter(**filter_params)
                
                if not relationships.exists():
                    raise VisaRelationship.DoesNotExist
                
                response_data = {
                    'success': True,
                    'search_type': search_type,
                    'title': f"{'Visa-Free' if search_type == 'visa_free' else 'ETA/eVisa'} Countries for {relationships.first().citizenship_country.name} Citizens",
                    'results': [format_visa_info(rel) for rel in relationships]
                }
            else:
                visa_info = base_query.get(destination_country__iso_code_2=to_country)
                response_data = {
                    'success': True,
                    'search_type': 'specific',
                    'title': f"Visa Requirements from {visa_info.citizenship_country.name} to {visa_info.destination_country.name}",
                    'results': [format_visa_info(visa_info)]
                }
            
            print("\nSending response:", response_data)
            
        except VisaRelationship.DoesNotExist:
            response_data = {
                'success': False,
                'error': 'No visa information found for these countries'
            }
        except Exception as e:
            print(f"\nError occurred: {str(e)}")
            response_data = {
                'success': False,
                'error': 'An error occurred while processing your request'
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

    # GET request - render initial page, country, program level, field of study, tuition range, additional filters, are added in the admin
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
        
        # Get active service plans ordered by their defined order
        service_plans = StudyServicePlan.objects.filter(
            is_active=True
        ).prefetch_related(
            'features',
            'included_services'
        )

        # Format plans for template
        context['service_plans'] = {
            plan.plan_type: {
                'name': plan.name,
                'description': plan.description,
                'price': plan.price,
                'timeline': plan.timeline,
                'features': [
                    feature.feature 
                    for feature in plan.features.all().order_by('order')
                ],
                'included_services': [
                    service.service 
                    for service in plan.included_services.all().order_by('order')
                ],
                'button_text': plan.button_text,
                'button_url': plan.button_url,
            }
            for plan in service_plans
        }

        return context


@method_decorator(login_required, name='dispatch')
class StudyAbroadSubscriptionView(View):
    """Handle Study Abroad subscription selection."""
    
    def get(self, request, *args, **kwargs):
        # Get the Study Abroad subscription plan
        plan = get_object_or_404(
            SubscriptionPlan,
            name='Study Abroad',
            is_active=True
        )
        
        # Redirect to subscription purchase with return URL
        return_url = reverse('tools:study_abroad_success')
        purchase_url = f"{reverse('subscriptions:plan_purchase', args=[plan.id])}?return_url={return_url}"
        
        return redirect(purchase_url)


@method_decorator(login_required, name='dispatch')
class StudyProgramSubscriptionView(View):
    """Handle Study Program subscription selection."""
    
    def get(self, request, *args, **kwargs):
        # Get the Study Program subscription plan
        plan = get_object_or_404(
            SubscriptionPlan,
            name='Study Program',
            is_active=True
        )
        
        # Redirect to subscription purchase with return URL
        return_url = reverse('tools:study_program_success')
        purchase_url = f"{reverse('subscriptions:plan_purchase', args=[plan.id])}?return_url={return_url}"
        
        return redirect(purchase_url)        
    

# Success views for after subscription
@login_required
def study_abroad_success(request):
    """Handle successful Study Abroad subscription."""
    return render(request, 'tools/study_abroad_success.html')


@login_required
def study_program_success(request):
    """Handle successful Study Program subscription."""
    return render(request, 'tools/study_program_success.html')    

