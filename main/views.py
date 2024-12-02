from django.shortcuts import render
from django.utils import timezone
from news.models import News  # Import the News model

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
    pass


def contact(request):
    pass


def services(request):
    return render(request, 'home/all-services.html')


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