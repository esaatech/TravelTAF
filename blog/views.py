from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404
from django.db.models import Count, Q
from .models import BlogPost, BlogCategory
# Create your views here.

def blog_list(request):
    posts = BlogPost.objects.filter(status='PUBLISHED').order_by('-published_at')
    categories = BlogCategory.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='PUBLISHED'))
    ).all()
    
    # Pagination
    paginator = Paginator(posts, 10)  # 10 posts per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'blog/post_list.html', {
        'posts': page_obj,
        'categories': categories,
        'is_paginated': paginator.num_pages > 1,
        'page_obj': page_obj,
    })

def nav_categories(request):
    categories = BlogCategory.objects.annotate(
        post_count=Count('posts', filter=Q(posts__status='PUBLISHED'))
    ).all()
    
    return render(request, 'blog/partials/nav_categories.html', {
        'categories': categories
    })

def category_detail(request, slug):
    category = get_object_or_404(BlogCategory, slug=slug)
    posts = BlogPost.objects.filter(category=category, status='PUBLISHED')
    return render(request, 'blog/category_detail.html', {
        'category': category,
        'posts': posts
    })

def post_detail(request, slug):
    post = get_object_or_404(BlogPost, slug=slug, status='PUBLISHED')
    return render(request, 'blog/post_detail.html', {
        'post': post
    })   