from django.shortcuts import render
from django.utils import timezone

def home(request):
    context = {
        'title': 'Welcome to TravelTAF',
        'current_year': timezone.now().year,
        'featured_destinations': [
            {
                'name': 'Paris',
                'country': 'France',
                'description': 'The City of Light'
            },
            {
                'name': 'Tokyo',
                'country': 'Japan',
                'description': 'A blend of modern and traditional'
            },
            {
                'name': 'New York',
                'country': 'USA',
                'description': 'The City That Never Sleeps'
            },
        ]
    }
    return render(request, 'home/home.html', context)


def about(request):
    pass


def contact(request):
    pass