from django.urls import path
from . import views

urlpatterns = [
    path('submit-study-abroad/', views.submit_study_abroad_form, name='submit_study_abroad'),
    path('submit-moving-abroad/', views.submit_moving_abroad_form, name='submit_moving_abroad'),
    path('api/register/', views.register_user, name='register_user'),
]
