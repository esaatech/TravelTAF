from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from .models import Resume
from .forms import ResumeForm
import json
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field
from typing import List

class OptimizedResume(BaseModel):
    optimized_content: str = Field(description="The ATS-optimized resume content")
    keyword_matches: List[str] = Field(description="List of important keywords matched from job description")
    improvement_suggestions: List[str] = Field(description="List of suggestions for improving the resume")
    ats_score: int = Field(description="ATS compatibility score out of 100")

class ResumeOptimizer:
    def __init__(self, api_key: str):
        self.llm = ChatOpenAI(
            temperature=0.1,
            model_name="gpt-4",
            openai_api_key=api_key
        )
        self.output_parser = PydanticOutputParser(pydantic_object=OptimizedResume)

    def optimize(self, resume_text: str, job_description: str) -> OptimizedResume:
        template = """
        You are an expert ATS (Applicant Tracking System) optimization specialist and professional resume writer.
        Analyze the provided resume and job description, then optimize the resume for ATS compatibility while 
        maintaining a professional tone.

        Resume:
        {resume_text}

        Job Description:
        {job_description}

        Please optimize the resume by:
        1. Identifying and incorporating relevant keywords from the job description
        2. Improving formatting for ATS readability
        3. Enhancing bullet points to better match job requirements
        4. Maintaining professional language and tone
        5. Ensuring proper section organization

        {format_instructions}
        """

        prompt = ChatPromptTemplate.from_template(template)
        
        messages = prompt.format_messages(
            resume_text=resume_text,
            job_description=job_description,
            format_instructions=self.output_parser.get_format_instructions()
        )

        response = self.llm.predict_messages(messages)
        return self.output_parser.parse(response.content)

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
