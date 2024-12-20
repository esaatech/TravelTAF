from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Resume
from .forms import ResumeForm
import json

def resume_home(request):
    return render(request, 'resume_builder/home.html')


def create_resume(request):
    # Hero section content
    hero_content = {
        'title': 'Resume Builder & Optimizer',
        'description': 'Create or optimize your ATS-friendly resume with our professional templates and AI-powered suggestions. Stand out to employers and increase your chances of getting hired.',
        'buttons': {
            'create': 'Create New Resume',
            'optimize': 'Optimize Existing Resume',
            'job_service': 'Job Application Service'
        },
        'credits_text': 'Credits per resume creation or optimization'
    }

    context = {
        'form': ResumeForm(),
        'hero_content': hero_content,
        'resume_services': {
            'builder_cost': 10  # or whatever the cost is
        }
    }

    return render(request, 'resume.html', context)


def optimize_resume(request):
    if request.method == 'POST':
        # Handle resume optimization
        pass
    return render(request, 'optimize.html')


def download_resume(request, resume_id):
    # Handle resume download
    pass
