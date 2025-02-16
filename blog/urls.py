from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.blog_list, name='post_list'),
    path('nav/categories/', views.nav_categories, name='nav_categories'),
    path('category/<slug:slug>/', views.category_detail, name='category'),
    path('post/<slug:slug>/', views.post_detail, name='post_detail'),
    path('ai-writer/', views.ai_writer_dashboard, name='ai_writer_dashboard'),
    path('ai-writer/write/', views.ai_write_post, name='ai_write_post'),
    path('ai-writer/update/<int:post_id>/', views.ai_update_post, name='ai_update_post'),
    path('ai-writer/publish/<int:post_id>/', views.ai_publish_post, name='ai_publish_post'),
    path('ai-writer/draft/<int:post_id>/', views.ai_save_draft, name='ai_save_draft'),
]   