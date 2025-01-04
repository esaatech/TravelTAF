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
    
    path('get-started/', views.get_started, name='get_started'),
    path('learn-more/', views.learn_more, name='learn_more'),
    # About page
    path('about/', views.about, name='about'),
    



]
