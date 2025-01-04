from django.urls import path
from . import views

app_name = 'faqs'

urlpatterns = [  # Make sure this list exists and is named exactly 'urlpatterns'
    path('', views.FAQListView.as_view(), name='faq_list'),
    # ... other URL patterns ...
]
