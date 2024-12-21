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


@login_required
def optimize_resume(request):
    hero_content = {
        'page_title': 'Optimize Your Resume',
        'page_description': 'Upload your resume and job description to create an ATS-optimized version tailored to the position.'
    }
    
    if request.method == 'POST':
        resume_file = request.FILES.get('resume_file')
        resume_text = request.POST.get('resume_text')
        job_description = request.POST.get('job_description')
        
        try:
            # Here you would add your resume optimization logic
            optimized_resume = Resume.objects.create(
                user=request.user,
                original_content=resume_text or resume_file.read().decode('utf-8'),
                job_description=job_description,
                # Add optimized content after processing
            )
            return redirect('download_resume', resume_id=optimized_resume.id)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
    
    return render(request, 'resume_builder/optimize_resume.html', {'hero_content': hero_content})


def download_resume(request, resume_id):
    # Handle resume download
    pass
