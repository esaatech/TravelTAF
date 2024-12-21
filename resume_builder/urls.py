from django.urls import path
from . import views

app_name = 'resume_builder'

urlpatterns = [
    path('', views.resume_home, name='home'),
    path('create-resume/', views.create_resume, name='create_resume'),
    path('optimize/', views.optimize_resume, name='optimize_resume'),
    path('download/', views.download_resume, name='download_resume'),
    path('download-pdf/', views.download_pdf, name='download_pdf'),
    path('download-word/', views.download_word, name='download_word'),
    path('save-resume/', views.save_resume, name='save_resume'),

]