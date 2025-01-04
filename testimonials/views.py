from django.shortcuts import render
from django.views.generic import ListView, CreateView
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import Testimonial
from .forms import TestimonialForm
from django.db.models import Q

class TestimonialCreateView(LoginRequiredMixin, CreateView):
    model = Testimonial
    form_class = TestimonialForm
    template_name = 'testimonials/testimonial_form.html'
    success_url = reverse_lazy('testimonials:testimonial_list')

    def form_valid(self, form):
        form.instance.is_active = False  # Require admin approval
        form.instance.initials = ''.join(word[0].upper() for word in self.request.user.get_full_name().split())
        messages.success(self.request, 'Thank you for your testimonial! It will be visible after review.')
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['rating_choices'] = Testimonial.RATING_CHOICES
        context['service_choices'] = Testimonial.SERVICE_CHOICES
        return context

class TestimonialListView(ListView):
    model = Testimonial
    template_name = 'testimonials/testimonial_list.html'
    context_object_name = 'testimonials'
    paginate_by = 9

    def get_queryset(self):
        queryset = Testimonial.objects.filter(is_active=True)
        
        testimonial_type = self.request.GET.get('type')
        rating = self.request.GET.get('rating')
        search = self.request.GET.get('search')

        if testimonial_type:
            queryset = queryset.filter(testimonial_type=testimonial_type)
        if rating:
            queryset = queryset.filter(rating=rating)
        if search:
            queryset = queryset.filter(
                Q(name__icontains=search) |
                Q(testimonial_text__icontains=search) |
                Q(location__icontains=search)
            )
        return queryset.order_by('-created_at')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['service_choices'] = Testimonial.SERVICE_CHOICES
        context['rating_choices'] = Testimonial.RATING_CHOICES
        return context

def testimonial_api(request):
    testimonials = Testimonial.objects.filter(is_active=True).values(
        'name', 
        'initials', 
        'location', 
        'rating', 
        'testimonial_text', 
        'testimonial_type', 
        'duration'
    )
    return JsonResponse({'testimonials': list(testimonials)})