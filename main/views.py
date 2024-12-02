from django.shortcuts import render
from django.utils import timezone
from news.models import News  # Import the News model

def home(request):
    # Query the latest 3 news articles
    latest_news = News.objects.filter(is_published=True).order_by('-published_date')[:3]

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
        ],
        'latest_news': latest_news  # Add the latest news to the context
    }
    return render(request, 'home/home.html', context)


def about(request):
    pass


def contact(request):
    pass


def services(request):
    return render(request, 'home/all-services.html')