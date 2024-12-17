from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import News, NewsCategory
from django_ckeditor_5.fields import CKEditor5Field

class ContentBlockInlineFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()
        # Validate content blocks structure
        for form in self.forms:
            if form.cleaned_data:
                block_type = form.cleaned_data.get('block_type')
                content = form.cleaned_data.get('content')
                # Add validation logic here

class NewsAdminForm(forms.ModelForm):
    class Meta:
        model = News
        fields = '__all__'
        widgets = {
            'summary': forms.Textarea(attrs={'rows': 3}),
            'content_blocks': forms.HiddenInput()  # Will be managed by custom JS
        }

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    form = NewsAdminForm
    list_display = ('title', 'published_date', 'is_featured', 'is_published')
    list_filter = ('is_featured', 'is_published', 'category')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'author', 'featured_image')
        }),
        ('Content', {
            'fields': ('summary', 'content')
        }),
        ('Publishing', {
            'fields': ('is_featured', 'is_published')
        }),
        ('Source', {
            'fields': ('source_name', 'source_url'),
            'classes': ('collapse',)
        }),
    )

    class Media:
        css = {
            'all': ('admin/css/content-blocks.css',)
        }
        js = ('admin/js/content-blocks.js',)

    def save_model(self, request, obj, form, change):
        # Process content blocks before saving
        if 'content_blocks' in form.cleaned_data:
            blocks = form.cleaned_data['content_blocks']
            # Add any processing logic here
        super().save_model(request, obj, form, change)
