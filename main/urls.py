from django.urls import path
from . import views

app_name = 'main'  # This enables namespacing for your URLs

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # Privacy Policy page
    path('privacypolicy/', views.privacypolicy, name='privacypolicy'),

    # Cookies page
    path('cookies/', views.cookies, name='cookies'),

    # Terms of Service page
    path('terms/', views.terms, name='terms'),

    # Compare Countries page
    path('compare-countries/', views.compare_countries, name='compare_countries'),  
    
    path('api/contact', views.contact_submit, name='contact_submit'),
    
    # urls.py
   path('api/compare', views.get_country_data, name='compare_countries_api'),
    # Contact page
    path('contact/', views.contact, name='contact'),
    
    # Services page
    path('services/', views.services, name='services'),
    path('services/moving-abroad/', views.moving_abroad, name='moving_abroad'),
    path('services/study-abroad/', views.study_abroad, name='study_abroad'),
    path('services/work-visas/', views.work_visas, name='work_visas'),
    
    # New paths for remaining services
    path('services/permanent-residency/', views.permanent_residency, name='permanent_residency'),
    path('services/family-sponsorship/', views.family_sponsorship, name='family_sponsorship'),
    path('services/travel-planning/', views.travel_planning, name='travel_planning'),
    path('get-started/', views.get_started, name='get_started'),
    path('learn-more/', views.learn_more, name='learn_more'),
    # About page
    path('about/', views.about, name='about'),
    path('travel-tours/', views.travel_tours, name='travel_tours'),
# Add these to your existing urlpatterns
path(
    'study-abroad-basic-report/',
    views.StudyAbroadBasicReportView.as_view(),
    name='study_abroad_basic_report'
),
path(
    'study-abroad-premium-report/',
    views.StudyAbroadPremiumReportView.as_view(),
    name='study_abroad_premium_report'
),
path(
    'study-abroad/basic/success/',
    views.study_abroad_basic_success,
    name='study_abroad_basic_success'
),
path(
    'study-abroad/premium/success/',
    views.study_abroad_premium_success,
    name='study_abroad_premium_success'
),



]
