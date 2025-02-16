from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from .models import BlogPost, BlogCategory
from .services.ai_writer import AIBlogWriter
from django.utils import timezone
from django_ckeditor_5.widgets import CKEditor5Widget
from django import forms
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib import admin
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

@staff_member_required
def ai_writer_dashboard(request):
    # If superuser, show all posts, otherwise filter by author
    if request.user.is_superuser:
        drafts = BlogPost.objects.filter(
            status='DRAFT'
        ).order_by('-created_at')
        
        published = BlogPost.objects.filter(
            status='PUBLISHED'
        ).order_by('-created_at')
    else:
        drafts = BlogPost.objects.filter(
            author=request.user,
            status='DRAFT'
        ).order_by('-created_at')
        
        published = BlogPost.objects.filter(
            author=request.user,
            status='PUBLISHED'
        ).order_by('-created_at')
    
    return render(request, 'blog/ai_writer/dashboard.html', {
        'drafts': drafts,
        'published': published,
        'is_superuser': request.user.is_superuser
    })

@staff_member_required
def ai_write_post(request):
    if request.method == 'POST':
        topic = request.POST.get('topic')
        category_id = request.POST.get('category')
        tone = request.POST.get('tone', 'informative')
        
        try:
            # Add logging to debug
            print(f"Received request - Topic: {topic}, Category: {category_id}, Tone: {tone}")
            
            category = BlogCategory.objects.get(id=category_id)
            ai_writer = AIBlogWriter()
            
            # Add more detailed error catching
            try:
                generated_content = ai_writer.generate_post(topic, category.name, tone)
            except Exception as e:
                print(f"AI Generation Error: {str(e)}")
                messages.error(request, f'Error in AI generation: {str(e)}')
                return redirect('blog:ai_write_post')
            
            # Verify generated content - now only checking for title and content
            if not generated_content or not all(key in generated_content for key in ['title', 'content']):
                print("Invalid generated content structure")
                messages.error(request, 'Invalid content generated')
                return redirect('blog:ai_write_post')
            
            # Create the post
            post = BlogPost.objects.create(
                title=generated_content['title'],
                content=generated_content['content'],
                category=category,
                author=request.user,
                status='DRAFT'
            )
            
            messages.success(request, 'Blog post generated successfully!')
            # Redirect to admin change page for the new post
            return redirect(f'/admin/blog/blogpost/{post.id}/change/')
            
        except BlogCategory.DoesNotExist:
            print(f"Category not found: {category_id}")
            messages.error(request, 'Selected category not found')
            return redirect('blog:ai_write_post')
        except Exception as e:
            messages.error(request, f'Error generating post: {str(e)}')
            return redirect('blog:ai_write_post')
    
    categories = BlogCategory.objects.all()
    return render(request, 'blog/ai_writer/write.html', {
        'categories': categories
    })

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['title', 'category', 'content', 'excerpt', 'featured_image']
        widgets = {
            'content': CKEditor5Widget(
                attrs={'class': 'django_ckeditor_5'}, 
                config_name='default'
            )
        }

@staff_member_required
def ai_update_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is superuser or the author
    if not request.user.is_superuser and post.author != request.user:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('blog:ai_writer_dashboard')
    
    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Blog post updated successfully!')
            return redirect('blog:ai_writer_dashboard')
    else:
        form = BlogPostForm(instance=post)
    
    return render(request, 'blog/ai_writer/update.html', {
        'form': form,
        'post': post,
        'categories': BlogCategory.objects.all()
    })

@staff_member_required
def ai_publish_post(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is superuser or the author
    if not request.user.is_superuser and post.author != request.user:
        messages.error(request, "You don't have permission to publish this post.")
        return redirect('blog:ai_writer_dashboard')
    
    post.status = 'PUBLISHED'
    post.published_at = timezone.now()
    post.save()
    
    messages.success(request, 'Blog post published successfully!')
    return redirect('blog:ai_writer_dashboard')

@staff_member_required
def ai_save_draft(request, post_id):
    post = get_object_or_404(BlogPost, id=post_id)
    
    # Check if user is superuser or the author
    if not request.user.is_superuser and post.author != request.user:
        messages.error(request, "You don't have permission to edit this post.")
        return redirect('blog:ai_writer_dashboard')
    
    post.status = 'DRAFT'
    post.save()
    
    messages.success(request, 'Blog post saved as draft!')
    return redirect('blog:ai_writer_dashboard')   