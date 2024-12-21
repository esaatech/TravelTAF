from django.shortcuts import render
from django.utils import timezone
from news.models import News  # Import the News model
from credits.models import CreditTransaction, UserCredit
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse

def home(request):
    # Query the latest 3 news articles
    latest_news = News.objects.filter(is_published=True).order_by('-published_date')[:3]

    context = {
        'title': 'Welcome to TravelTAF',
        'current_year': timezone.now().year,
        'featured_destinations': [
            {
                'name': 'Paris',
                'country': 'France',
                'description': 'The City of Light'
            },
            {
                'name': 'Tokyo',
                'country': 'Japan',
                'description': 'A blend of modern and traditional'
            },
            {
                'name': 'New York',
                'country': 'USA',
                'description': 'The City That Never Sleeps'
            },
        ],
        'latest_news': latest_news  # Add the latest news to the context
    }
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    pass


def services(request):
    return render(request, 'home/all-services.html')

from django.http import JsonResponse

def contact_submit(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        
        try:
            # Add your email sending logic here
            # You might want to use Django's send_mail or a third-party service
            
            return JsonResponse({
                'status': 'success',
                'message': 'Thank you for your message. We will get back to you soon!'
            })
        except Exception as e:
            return JsonResponse({
                'status': 'error',
                'message': 'Sorry, there was an error sending your message.'
            }, status=500)
    
    return JsonResponse({'message': 'Invalid request method'}, status=400)

def moving_abroad(request):
    context = {
        'page_title': 'Moving Abroad Guide',
        'page_description': 'Discover different pathways and options for moving abroad',
        
        'pathways': {
            'education': {
                'title': 'Education Route',
                'icon': 'M12 14l9-5-9-5-9 5 9 5z',  # Graduation cap icon
                'options': [
                    {'name': 'Student Visas', 'description': 'Full-time study at recognized institutions'},
                    {'name': 'Language Schools', 'description': 'Language study programs and cultural exchange'},
                    {'name': 'Exchange Programs', 'description': 'Academic and cultural exchange opportunities'},
                    {'name': 'Post-Study Work', 'description': 'Work opportunities after graduation'},
                ]
            },
            'employment': {
                'title': 'Employment Route',
                'icon': 'M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z',  # Briefcase icon
                'options': [
                    {'name': 'Work Visas', 'description': 'Employment-based immigration options'},
                    {'name': 'Skilled Migration', 'description': 'Programs for qualified professionals'},
                    {'name': 'Digital Nomad Visas', 'description': 'Remote work opportunities abroad'},
                    {'name': 'Working Holiday', 'description': 'Temporary work and travel programs'},
                ]
            },
            'family': {
                'title': 'Family Route',
                'icon': 'M17 20h5v-2a3 3 0 00-5.356-1.857M17 20H7m10 0v-2c0-.656-.126-1.283-.356-1.857M7 20H2v-2a3 3 0 015.356-1.857M7 20v-2c0-.656.126-1.283.356-1.857m0 0a5.002 5.002 0 019.288 0M15 7a3 3 0 11-6 0 3 3 0 016 0zm6 3a2 2 0 11-4 0 2 2 0 014 0zM7 10a2 2 0 11-4 0 2 2 0 014 0z',  # Family icon
                'options': [
                    {'name': 'Family Reunification', 'description': 'Join family members abroad'},
                    {'name': 'Partner/Spouse Visas', 'description': 'Marriage and partnership-based options'},
                    {'name': 'Parent Visas', 'description': 'Options for parents and guardians'},
                    {'name': 'Child Dependent Visas', 'description': 'Programs for dependent children'},
                ]
            },
            'investment': {
                'title': 'Investment Route',
                'icon': 'M12 8c-1.657 0-3 .895-3 2s1.343 2 3 2 3 .895 3 2-1.343 2-3 2m0-8c1.11 0 2.08.402 2.599 1M12 8V7m0 1v8m0 0v1m0-1c-1.11 0-2.08-.402-2.599-1M21 12a9 9 0 11-18 0 9 9 0 0118 0z',  # Money icon
                'options': [
                    {'name': 'Business Visas', 'description': 'For business owners and entrepreneurs'},
                    {'name': 'Investor Programs', 'description': 'Investment-based immigration options'},
                    {'name': 'Start-up Visas', 'description': 'Programs for innovative businesses'},
                ]
            },
            'special': {
                'title': 'Special Categories',
                'icon': 'M11.049 2.927c.3-.921 1.603-.921 1.902 0l1.519 4.674a1 1 0 00.95.69h4.915c.969 0 1.371 1.24.588 1.81l-3.976 2.888a1 1 0 00-.363 1.118l1.518 4.674c.3.922-.755 1.688-1.538 1.118l-3.976-2.888a1 1 0 00-1.176 0l-3.976 2.888c-.783.57-1.838-.197-1.538-1.118l1.518-4.674a1 1 0 00-.363-1.118l-3.976-2.888c-.784-.57-.38-1.81.588-1.81h4.914a1 1 0 00.951-.69l1.519-4.674z',  # Star icon
                'options': [
                    {'name': 'Retirement Visas', 'description': 'Programs for retirees'},
                    {'name': 'Religious Worker Visas', 'description': 'For religious and charitable work'},
                    {'name': 'Volunteer Visas', 'description': 'Humanitarian and volunteer opportunities'},
                    {'name': 'Artist/Cultural Visas', 'description': 'For artists and performers'},
                ]
            },
            'humanitarian': {
                'title': 'Humanitarian Protection',
                'icon': 'M4.318 6.318a4.5 4.5 0 000 6.364L12 20.364l7.682-7.682a4.5 4.5 0 00-6.364-6.364L12 7.636l-1.318-1.318a4.5 4.5 0 00-6.364 0z',  # Heart icon
                'options': [
                    {
                        'name': 'Asylum',
                        'description': 'Protection for those fleeing persecution in their home country'
                    },
                    {
                        'name': 'Refugee Status',
                        'description': 'UN-recognized refugee resettlement programs'
                    },
                    {
                        'name': 'Humanitarian Visas',
                        'description': 'Special programs for humanitarian circumstances'
                    },
                    {
                        'name': 'Temporary Protected Status',
                        'description': 'Temporary protection for specific country conditions'
                    }
                ],
                'note': 'These options are for individuals seeking protection from persecution or serious harm. Please consult official government resources or legal professionals for specific guidance.'
            }
        },
        
        'consultation_services': {
            'pathway_assessment': {
                'title': 'Pathway Assessment',
                'credits': 25,
                'description': 'Personal review and recommendations for your best moving abroad options'
            },
            'detailed_consultation': {
                'title': 'Detailed Consultation',
                'credits': 40,
                'description': 'In-depth planning and guidance for your chosen pathway'
            },
            'document_strategy': {
                'title': 'Document Strategy',
                'credits': 20,
                'description': 'Comprehensive document preparation guide and timeline'
            }
        }
    }
    return render(request, 'services/moving_abroad.html', context)


def immigration_consulting(request):
    context = {
        'service': {
            'title': 'Immigration Consulting',
            'description': 'Expert guidance through your immigration journey with personalized solutions and support.',
            'features': [
                {
                    'title': 'Visa Assessment',
                    'description': 'Comprehensive evaluation of your eligibility for various immigration pathways.',
                    'icon': 'document'
                },
                {
                    'title': 'Documentation Support',
                    'description': 'Complete assistance with preparing and organizing required documents.',
                    'icon': 'folder'
                },
                {
                    'title': 'Application Processing',
                    'description': 'End-to-end support for your immigration application process.',
                    'icon': 'application'
                }
            ],
            'process_steps': [
                {
                    'step': 1,
                    'title': 'Initial Consultation',
                    'description': 'Free assessment of your immigration options'
                },
                {
                    'step': 2,
                    'title': 'Strategy Development',
                    'description': 'Create a personalized immigration plan'
                },
                {
                    'step': 3,
                    'title': 'Documentation',
                    'description': 'Prepare and verify all required documents'
                },
                {
                    'step': 4,
                    'title': 'Application Filing',
                    'description': 'Submit and monitor your application'
                }
            ],
            'packages': [
                {
                    'name': 'Basic',
                    'price': '899',
                    'features': [
                        'Initial Consultation',
                        'Eligibility Assessment',
                        'Basic Document Review'
                    ],
                    'is_featured': False
                },
                {
                    'name': 'Standard',
                    'price': '1,699',
                    'features': [
                        'All Basic Features',
                        'Full Documentation Support',
                        'Application Filing',
                        'Case Monitoring'
                    ],
                    'is_featured': True
                },
                {
                    'name': 'Premium',
                    'price': '2,899',
                    'features': [
                        'All Standard Features',
                        'Priority Processing',
                        'Appeal Support',
                        'Post-Landing Services'
                    ],
                    'is_featured': False
                }
            ],
            'faqs': [
                {
                    'question': 'What documents do I need for immigration?',
                    'answer': '''Common required documents include:
                        • Valid Passport
                        • Educational Credentials
                        • Work Experience Letters
                        • Language Test Results
                        • Police Clearance Certificates'''
                },
                {
                    'question': 'How long does the immigration process take?',
                    'answer': "Processing times vary by program and country, typically ranging from 6-12 months. We'll provide specific timelines based on your immigration pathway."
                },
                {
                    'question': 'What are my chances of success?',
                    'answer': "Success rates depend on various factors including your qualifications, chosen immigration program, and application completeness. We'll assess your eligibility and recommend the most suitable pathway."
                }
            ],
            'success_stories': [
                {
                    'name': 'John Smith',
                    'institution': 'Permanent Resident in Canada',
                    'image': 'testimonials/client-1.jpg',
                    'testimonial': "TravelTAF's expertise made my immigration journey smooth and successful. Their attention to detail and constant support were invaluable."
                },
                {
                    'name': 'Emily Wong',
                    'institution': 'Family Immigration to Australia',
                    'image': 'testimonials/client-2.jpg',
                    'testimonial': "Thanks to TravelTAF, our family's dream of moving to Australia became a reality. Their comprehensive support made the complex process manageable."
                },
                {
                    'name': 'Ahmed Hassan',
                    'institution': 'Skilled Migration to New Zealand',
                    'image': 'testimonials/client-3.jpg',
                    'testimonial': "The team's knowledge of New Zealand's immigration system was impressive. They guided me through every step of the skilled migration process."
                }
            ],
            'cta': {
                'title': 'Ready to Start Your Immigration Journey?',
                'subtitle': 'Schedule your free consultation today',
                'primary_button': {
                    'text': 'Book Consultation',
                    'url': '/contact/'
                },
                'secondary_button': {
                    'text': 'Download Guide',
                    'url': '/resources/immigration-guide/'
                }
            }
        }
    }
    
    return render(request, 'services/immigration_consulting.html', context)


def study_abroad(request):
    context = {
        'service': {
            'title': 'Study Abroad',
            'description': 'Transform your future with international education opportunities. Expert guidance for university admissions and student visas.',
            'features': [
                {
                    'title': 'University Selection',
                    'description': 'Expert guidance in choosing the right university and program based on your goals.',
                    'icon': 'university'  # You can define SVG icons in the template
                },
                {
                    'title': 'Application Support', 
                    'description': 'Complete assistance with university applications and documentation.',
                    'icon': 'document'
                },
                {
                    'title': 'Student Visa',
                    'description': 'Complete visa application support and guidance for international students.',
                    'icon': 'visa'
                }
            ],
            'process_steps': [
                {
                    'step': 1,
                    'title': 'Initial Assessment',
                    'description': 'Evaluate academic background and goals'
                },
                {
                    'step': 2,
                    'title': 'University Selection',
                    'description': 'Choose suitable universities and programs'
                },
                {
                    'step': 3,
                    'title': 'Application Submission',
                    'description': 'Prepare and submit university applications'
                },
                {
                    'step': 4,
                    'title': 'Visa Application',
                    'description': 'Student visa application and documentation'
                }
            ],
            'packages': [
                {
                    'name': 'Basic',
                    'price': '999',
                    'features': [
                        'Initial Consultation',
                        'University Selection',
                        'Basic Application Support'
                    ],
                    'is_featured': False
                },
                {
                    'name': 'Premium',
                    'price': '1,999',
                    'features': [
                        'All Basic Features',
                        'Priority Support',
                        'Visa Application Support'
                    ],
                    'is_featured': True
                },
                {
                    'name': 'Elite',
                    'price': '2,999',
                    'features': [
                        'All Premium Features',
                        'Accommodation Support',
                        'Post-Landing Support'
                    ],
                    'is_featured': False
                }
            ],
            'faqs': [
                {
                    'question': 'What are the basic requirements for studying abroad?',
                    'answer': '''Generally, you'll need:
                        • Academic transcripts
                        • Language proficiency test scores (IELTS/TOEFL)
                        • Letter of recommendation
                        • Statement of purpose
                        • Valid passport'''
                },
                {
                    'question': 'How long does the application process take?',
                    'answer': 'The application process typically takes 3-6 months, including university application and visa processing. We recommend starting at least 8-12 months before your intended start date.'
                },
                {
                    'question': 'What kind of scholarships are available?',
                    'answer': '''Various scholarships are available including:
                        • Merit-based scholarships
                        • Country-specific scholarships
                        • University grants
                        • Research fellowships
                        • Sport scholarships'''
                }
            ],
            'success_stories': [
                {
                    'name': 'Sarah Johnson',
                    'institution': 'University of Toronto',
                    'image': 'testimonials/student-1.jpg',
                    'testimonial': "TravelTAF made my dream of studying in Canada a reality. Their guidance throughout the application process was invaluable, and I'm now pursuing my Master's degree at my dream university!"
                },
                {
                    'name': 'Michael Chen',
                    'institution': 'University of Melbourne',
                    'image': 'testimonials/student-2.jpg',
                    'testimonial': "From university selection to visa approval, TravelTAF's team was there every step of the way. Their expertise in Australian education system was crucial for my success."
                },
                {
                    'name': 'Priya Patel',
                    'institution': 'University of British Columbia',
                    'image': 'testimonials/student-3.jpg',
                    'testimonial': "The scholarship guidance from TravelTAF helped me secure partial funding for my studies. Their comprehensive support made the entire process smooth and stress-free."
                }
            ],
            'cta': {
                'title': 'Ready to Begin Your International Education Journey?',
                'subtitle': 'Get a free consultation and discover your study abroad opportunities',
                'primary_button': {
                    'text': 'Book Free Consultation',
                    'url': '/contact/'
                },
                'secondary_button': {
                    'text': 'Download University Guide',
                    'url': '/resources/university-guide/'
                }
            }
        }
    }
    return render(request, 'services/study_abroad.html', context)


def work_visas(request):
    context = {
        'service': {
            'title': 'Work Visa Services',
            'description': 'Expert guidance for your work permit and visa applications. We help professionals and skilled workers secure employment opportunities abroad.',
            'features': [
                {
                    'title': 'Visa Assessment',
                    'description': 'Comprehensive evaluation of your eligibility for various work visas and permits.',
                    'icon': 'document'
                },
                {
                    'title': 'Job Search Support',
                    'description': 'Guidance on finding suitable job opportunities and employer sponsorship.',
                    'icon': 'search'
                },
                {
                    'title': 'Application Processing',
                    'description': 'Complete assistance with work permit and visa application documentation.',
                    'icon': 'application'
                }
            ],
            'process_steps': [
                {
                    'step': 1,
                    'title': 'Skills Assessment',
                    'description': 'Evaluate your qualifications and work experience'
                },
                {
                    'step': 2,
                    'title': 'Visa Category Selection',
                    'description': 'Identify the most suitable work visa pathway'
                },
                {
                    'step': 3,
                    'title': 'Documentation',
                    'description': 'Prepare and verify all required documents'
                },
                {
                    'step': 4,
                    'title': 'Visa Application',
                    'description': 'Submit application and track progress'
                }
            ],
            'packages': [
                {
                    'name': 'Basic',
                    'price': '799',
                    'features': [
                        'Initial Consultation',
                        'Eligibility Assessment',
                        'Basic Document Review'
                    ],
                    'is_featured': False
                },
                {
                    'name': 'Professional',
                    'price': '1,499',
                    'features': [
                        'All Basic Features',
                        'Job Search Guidance',
                        'Application Filing Support',
                        'Interview Preparation'
                    ],
                    'is_featured': True
                },
                {
                    'name': 'Executive',
                    'price': '2,499',
                    'features': [
                        'All Professional Features',
                        'Priority Processing',
                        'Post-Landing Support',
                        'Family Visa Support'
                    ],
                    'is_featured': False
                }
            ],
            'faqs': [
                {
                    'question': 'What types of work visas do you handle?',
                    'answer': '''We assist with various work visa categories including:
                        • Skilled Worker Visas
                        • Temporary Work Permits
                        • Employer-Sponsored Visas
                        • Professional Visas
                        • Working Holiday Visas'''
                },
                {
                    'question': 'How long does the work visa process take?',
                    'answer': 'Processing times vary by country and visa type, typically ranging from 2-6 months. Factors like employer sponsorship and document preparation can affect the timeline.'
                },
                {
                    'question': 'Do I need a job offer first?',
                    'answer': "This depends on the visa category and country. Some visas require a job offer and employer sponsorship, while others allow you to enter the country to seek employment. We'll help determine the best pathway based on your situation."
                }
            ],
            'success_stories': [
                {
                    'name': 'David Wilson',
                    'institution': 'Software Engineer in Canada',
                    'image': 'testimonials/professional-1.jpg',
                    'testimonial': "TravelTAF's expertise was invaluable in securing my work permit. Their step-by-step guidance made the complex process manageable."
                },
                {
                    'name': 'Maria Rodriguez',
                    'institution': 'Healthcare Professional in Australia',
                    'image': 'testimonials/professional-2.jpg',
                    'testimonial': "Thanks to TravelTAF, I successfully obtained my skilled worker visa. Their knowledge of healthcare sector requirements was impressive."
                },
                {
                    'name': 'James Chen',
                    'institution': 'Financial Analyst in UK',
                    'image': 'testimonials/professional-3.jpg',
                    'testimonial': "The team's attention to detail and expertise in UK work visas helped me achieve my career goals abroad."
                }
            ],
            'cta': {
                'title': 'Ready to Start Your International Career?',
                'subtitle': 'Get expert guidance for your work visa application',
                'primary_button': {
                    'text': 'Free Assessment',
                    'url': '/contact/'
                },
                'secondary_button': {
                    'text': 'Download Guide',
                    'url': '/resources/work-visa-guide/'
                }
            }
        }
    }
    
    return render(request, 'services/work_visa.html', context)


def permanent_residency(request):
    return render(request, 'services/permanent_residency.html')


def family_sponsorship(request):
    return render(request, 'services/family_sponsorship.html')


def travel_planning(request):
    return render(request, 'services/travel_planning.html')


def get_started(request):
    return render(request, 'home/get_started.html')


def learn_more(request):
    return render(request, 'home/learn_more.html')

def about(request):
    return render(request, 'home/about.html')

def privacypolicy(request):
    return render(request, 'home/privacypolicy.html')

def terms(request):
    return render(request, 'home/terms.html')

def cookies(request):
    return render(request, 'home/cookies.html')

@login_required
def dashboard(request):
    # Get user's credit balance
    user_credit = UserCredit.objects.filter(user=request.user).first()
    credit_balance = user_credit.balance if user_credit else 0

    # Get recent transactions
    recent_transactions = CreditTransaction.objects.filter(
        user=request.user
    ).order_by('-created_at')[:5]

    # Get user's display name (full name if available, otherwise username)
    display_name = request.user.get_full_name() or request.user.username

    context = {
        'recent_transactions': recent_transactions,
        'unread_notifications': request.user.notifications.unread().exists() if hasattr(request.user, 'notifications') else False,
        'credit_balance': credit_balance,
        'display_name': display_name,
    }
    
    return render(request, 'dashboard/dashboard.html', context)

def compare_countries(request):
    context = {
        'page_title': 'Compare Countries',
        'page_description': 'Make informed decisions by comparing key aspects of different countries for travel, study, or migration.',
        'countries': [
            {'code': 'ca', 'name': 'Canada'},
            {'code': 'au', 'name': 'Australia'},
            {'code': 'uk', 'name': 'United Kingdom'},
            # Add more countries as needed
        ]
    }
    return render(request, 'home/compare-countries.html', context)





def get_country_data(request):
    # Sample data structure
    country_data = {
        'ca': {
            'cost': {
                'rent': '$1,500',
                'food': '$500',
                'transport': '$150'
            },
            'tourism': {
                'attractions': 'Banff, Niagara Falls',
                'season': 'June-September',
                'visa': 'eTA required'
            },
            'immigration': {
                'work_visa': 'Express Entry',
                'study_permit': '20-30 days',
                'pr_options': 'CEC, FSW, PNP'
            }
        },
        'au': {
            'cost': {
                'rent': '$1,800',
                'food': '$600',
                'transport': '$170'
            },
            'tourism': {
                'attractions': 'Great Barrier Reef, Sydney Opera House',
                'season': 'December-February',
                'visa': 'ETA required'
            },
            'immigration': {
                'work_visa': 'Skilled Migration',
                'study_permit': '4-6 weeks',
                'pr_options': 'Points Based System'
            }
        }
    }
    
    country1 = request.GET.get('country1')
    country2 = request.GET.get('country2')
    
    return JsonResponse({
        'country1': country_data.get(country1),
        'country2': country_data.get(country2)
    })