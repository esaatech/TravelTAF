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
        'service_name': 'Immigration Consulting',
        'features': [
            {
                'title': 'Visa Assessment',
                'description': 'Comprehensive evaluation of your eligibility',
                'icon': 'assessment-icon'
            },
            # More features...
        ],
        'faqs': [
            {
                'question': 'What documents do I need?',
                'answer': 'Detailed answer...'
            },
            # More FAQs...
        ],
        'testimonials': [
            {
                'name': 'John Doe',
                'country': 'Canada',
                'content': 'Testimonial content...',
                'image': 'path/to/image'
            },
            # More testimonials...
        ],
        'packages': [
            {
                'name': 'Basic',
                'price': 'XXX',
                'features': ['Feature 1', 'Feature 2', ...]
            },
            # More packages...
        ]
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