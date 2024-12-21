from django.urls import path
from . import views

app_name = 'resume_builder'

urlpatterns = [
    path('', views.resume_home, name='home'),
    path('create-resume/', views.create_resume, name='create_resume'),
    path('optimize/', views.optimize_resume, name='optimize_resume'),
    path('download/<int:resume_id>/', views.download_resume, name='download'),
]