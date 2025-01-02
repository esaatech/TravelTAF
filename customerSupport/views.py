from django.shortcuts import render

# Create your views here.

def submit_study_abroad_form(request):
    return render(request, 'services/study_abroad.html')

def submit_moving_abroad_form(request):
    return render(request, 'services/moving_abroad.html')