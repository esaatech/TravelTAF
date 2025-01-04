from django.urls import path
from . import views

app_name = 'service_offerings'
    
    



urlpatterns = [
# Services page
    
    path('services/', views.services, name='services'),
    path('services/moving-abroad/', views.moving_abroad, name='moving_abroad'),
    path('services/study-abroad/', views.study_abroad, name='study_abroad'),
    path('services/work-visas/', views.work_visas, name='work_visas'),
    
    # New paths for remaining services
    path('services/permanent-residency/', views.permanent_residency, name='permanent_residency'),
    path('services/family-sponsorship/', views.family_sponsorship, name='family_sponsorship'),
    path('services/travel-planning/', views.travel_planning, name='travel_planning'),
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