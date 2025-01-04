from django.urls import path
from . import views

app_name = 'testimonials'

urlpatterns = [
    path('', views.TestimonialListView.as_view(), name='testimonial_list'),
    path('add/', views.TestimonialCreateView.as_view(), name='testimonial_add'),
    path('api/testimonials/', views.testimonial_api, name='testimonial_api'),
]


