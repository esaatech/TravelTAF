from django import forms
from .models import Testimonial

class TestimonialForm(forms.ModelForm):
    class Meta:
        model = Testimonial
        fields = ['name', 'location', 'testimonial_type', 'rating', 'testimonial_text']
        widgets = {
            'rating': forms.RadioSelect(choices=[(i, f'{i} Stars') for i in range(1, 6)]),
            'testimonial_text': forms.Textarea(attrs={'rows': 4, 'placeholder': 'Share your experience...'}),
        } 