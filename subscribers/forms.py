from django import forms
from .models import Subscriber

class SubscriberForm(forms.ModelForm):
    email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class': 'px-4 py-2 border border-gray-300 rounded-l-full focus:outline-none focus:border-[#1980e6] w-64',
                'placeholder': 'Enter your email'
            }
        )
    )
    subscription_type = forms.ChoiceField(
        choices=Subscriber.SUBSCRIPTION_TYPES,
        required=True,
        widget=forms.HiddenInput()
    )

    class Meta:
        model = Subscriber
        fields = ['email', 'subscription_type']
