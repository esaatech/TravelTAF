from django.views.generic import ListView, DetailView
from django.shortcuts import get_object_or_404
from .models import FAQ, Category

class FAQListView(ListView):
    model = FAQ
    template_name = 'faqs/faq_list.html'
    context_object_name = 'categories'

    def get_queryset(self):
        return Category.objects.filter(
            is_active=True
        ).prefetch_related(
            'faqs'
        ).order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['active_category'] = self.request.GET.get('category', '')
        return context

class CategoryFAQView(DetailView):
    model = Category
    template_name = 'faqs/category_faqs.html'
    context_object_name = 'category'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['faqs'] = self.object.faqs.filter(is_active=True).order_by('order')
        context['categories'] = Category.objects.filter(is_active=True)
        return context
