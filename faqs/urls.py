from django.urls import path
from . import views

app_name = 'faqs'

urlpatterns = [
    path('', views.FAQListView.as_view(), name='faq_list'),
    path('category/<slug:slug>/', views.CategoryFAQView.as_view(), name='category_detail'),
]
