from django.urls import path, include
from . import views

from django.urls import path
from .views import program_detail, program_list, country_programs

app_name = 'immigration'

urlpatterns = [
    # List all countries with immigration programs
    path("programs/", program_list, name="program_list"),
    
    # List all programs for a specific country
    path("programs/<slug:country_slug>/", country_programs, name="country_programs"),
    
    # Specific program detail
    path("programs/<slug:country_slug>/<slug:program_slug>/", program_detail, name="program_detail"),

    path('nav-programs/', views.immigration_nav_programs, name='nav_programs'),

    path('programs/<str:country_code>/', views.country_programs, name='country_programs'),
]