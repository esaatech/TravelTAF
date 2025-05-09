from django.shortcuts import render
from django.utils import timezone
from news.models import News  # Import the News model
from credits.models import CreditTransaction, UserCredit
from django.contrib.auth.decorators import login_required
from django.db.models import F
from django.http import JsonResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from tools.models import School
import json
import random
from django.views.generic import View
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.shortcuts import redirect
from subscriptions.models import SubscriptionPlan
from django.contrib.auth.mixins import LoginRequiredMixin
from testimonials.models import Testimonial  # Add this import
from faqs.models import Category, FAQ  # Add this import
from immigrationprograms.views import get_featured_immigration_data
from .models import TravelDestination
        
def home(request):
    # Query the latest 3 news articles that are both published and approved
    latest_news = News.objects.filter(
        is_published=True,
        status='APPROVED'
    ).order_by('-published_date')[:3]

    # Get active testimonials
    testimonials = Testimonial.objects.filter(
        is_active=True
    ).order_by('?')[:3]  # Random selection of 3 testimonials

    # Get FAQs for the home page
    featured_faqs = FAQ.objects.filter(
        is_active=True,
        category__is_active=True
    ).select_related('category').order_by('?')[:5]  # Random 5 FAQs

    # Get featured destinations
    featured_destinations = TravelDestination.objects.filter(
        is_active=True,
        is_featured=True
    ).order_by('order')[:3]

    # Get immigration data for featured destinations
    immigration_data = get_featured_immigration_data()

    context = {
        'title': 'Welcome to TravelTAF',
        'current_year': timezone.now().year,
        'featured_destinations': featured_destinations,
        'latest_news': latest_news,
        'testimonials': testimonials,
        'featured_faqs': featured_faqs,
        'immigration_data': immigration_data,
    }
    return render(request, 'home/home.html', context)


def about(request):
    return render(request, 'home/about.html')


def contact(request):
    pass




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


