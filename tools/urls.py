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
    path('generate-cover-letter/', views.generate_cover_letter, name='generate_cover_letter'),

]
