from django.urls import path
from . import views

app_name = 'main'  # This enables namespacing for your URLs

urlpatterns = [
    # Home page
    path('', views.home, name='home'),
    
    # About page
    path('about/', views.about, name='about'),
    
    # Contact page
    path('contact/', views.contact, name='contact'),
    
    # Services page
    path('services/', views.services, name='services'),
    path('services/immigration-consulting/', views.immigration_consulting, name='immigration_consulting'),
   path('services/study-abroad/', views.study_abroad, name='study_abroad'),
   # path('services/work-visas/', views.work_visas, name='work_visas'),
    
]