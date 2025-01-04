from django.views.generic import ListView
from django.shortcuts import render
from .models import FAQ

class FAQListView(ListView):
    model = FAQ
    template_name = 'faqs/faq_list.html'
    context_object_name = 'faqs'
    
    def get_queryset(self):
        return FAQ.objects.filter(is_active=True).order_by('category', 'order')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Group FAQs by category
        faqs_by_category = {}
        for faq in context['faqs']:
            if faq.category not in faqs_by_category:
                faqs_by_category[faq.category] = []
            faqs_by_category[faq.category].append(faq)
        context['faqs_by_category'] = faqs_by_category
        return context

# Optional: API view for AJAX loading
from django.http import JsonResponse

def faq_api(request):
    faqs = FAQ.objects.filter(is_active=True).values(
        'question', 
        'answer', 
        'category',
        'order'
    ).order_by('category', 'order')
    
    # Group FAQs by category
    faqs_by_category = {}
    for faq in faqs:
        category = faq['category']
        if category not in faqs_by_category:
            faqs_by_category[category] = []
        faqs_by_category[category].append({
            'question': faq['question'],
            'answer': faq['answer'],
            'order': faq['order']
        })
    
    return JsonResponse({'faqs': faqs_by_category})
