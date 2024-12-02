from django.urls import path
from . import views

app_name = 'news'

urlpatterns = [
    path('', views.NewsListView.as_view(), name='list'),
    path('category/<slug:category_slug>/', views.NewsListView.as_view(), name='category'),
    path('<slug:slug>/', views.NewsDetailView.as_view(), name='detail'),
]
