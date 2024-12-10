from django.urls import path
from . import views
 
app_name = 'tools'


urlpatterns = [
    path('visa-checker/', views.visa_checker, name='visa_checker'),
    path('points-calculator/', views.points_calculator, name='points_calculator'),
    path('cost-estimator/', views.cost_estimator, name='cost_estimator'),
    path('document-checker/', views.document_checker, name='document_checker'),
    path('timeline-planner/', views.timeline_planner, name='timeline_planner'),
    path('language-test/', views.language_test, name='language_test'),
    path('job-search/', views.job_search, name='job_search'),
    path('school-finder/', views.school_finder, name='school_finder'),
    path('job-cover-letter/', views.job_cover_letter, name='job_cover_letter'),
    path('visa-cover-letter/', views.visa_cover_letter, name='visa_cover_letter'),
    path('study-abroad-cover-letter/', views.study_abroad_cover_letter, name='study_abroad_cover_letter'),
    path('travel-sponsorship-cover-letter/', views.travel_sponsorship_cover_letter, name='travel_sponsorship_cover_letter'),
    path('immigration-support-cover-letter/', views.immigration_support_cover_letter, name='immigration_support_cover_letter'),
    path('tourist-invitation-cover-letter/', views.tourist_invitation_cover_letter, name='tourist_invitation_cover_letter'),
    path('cover-letters/', views.cover_letters, name='cover_letters'),
]
