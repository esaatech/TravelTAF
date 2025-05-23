from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html
from .models import BlogCategory, BlogPost

@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'get_post_count')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    def get_post_count(self, obj):
        return obj.posts.count()
    get_post_count.short_description = 'Posts'

@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'status', 'author', 'created_at', 'published_at')
    list_filter = ('status', 'category', 'created_at')
    search_fields = ('title', 'content', 'excerpt')
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    change_list_template = 'admin/blog/blogpost/change_list.html'
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'category', 'content', 'excerpt', 'featured_image')
        }),
        ('Publishing', {
            'fields': ('status', 'author', 'published_at')
        }),
    )
    
    def save_model(self, request, obj, form, change):
        if not obj.author:
            obj.author = request.user
        super().save_model(request, obj, form, change)

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context['ai_writer_url'] = reverse('blog:ai_writer_dashboard')
        return super().changelist_view(request, extra_context=extra_context)
