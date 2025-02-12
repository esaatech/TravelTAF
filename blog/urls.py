from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='post_list'),
    path('nav/categories/', views.nav_categories, name='nav_categories'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
]   