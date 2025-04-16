from django import forms
from django.contrib import admin
from django.utils.html import format_html
from .models import News, NewsCategory, DialogContent
from django_ckeditor_5.fields import CKEditor5Field
from django.utils import timezone
from django.urls import reverse
from django.utils.safestring import mark_safe

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
    list_display = ('title', 'published_date', 'is_featured', 'is_published', 'get_status', 'approval_actions')
    list_filter = ('is_featured', 'is_published', 'category', 'status')
    search_fields = ('title', 'summary')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('approved_by', 'approved_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('title', 'slug', 'category', 'author', 'featured_image')
        }),
        ('Content', {
            'fields': ('summary', 'content')
        }),
        ('Publishing', {
            'fields': ('is_featured', 'is_published', 'send_as_newsletter')
        }),
        ('Source', {
            'fields': ('source_name', 'source_url'),
            'classes': ('collapse',)
        }),
        ('Approval Information', {
            'fields': ('status', 'approved_by', 'approved_at', 'review_notes'),
            'classes': ('collapse',)
        }),
    )

    actions = ['approve_news', 'reject_news']

    def get_status(self, obj):
        status_classes = {
            'PENDING': 'status-pending',
            'APPROVED': 'status-approved',
            'REJECTED': 'status-rejected',
        }
        return format_html(
            '<span class="status-badge {}">{}</span>',
            status_classes.get(obj.status, ''),
            obj.get_status_display()
        )
    get_status.short_description = 'Status'

    def approval_actions(self, obj):
        if obj.status == 'PENDING':
            return format_html(
                '<a class="action-button approve-button" href="{}">'
                'Approve</a> '
                '<a class="action-button reject-button" href="{}">'
                'Reject</a>',
                reverse('admin:approve_news', args=[obj.pk]),
                reverse('admin:reject_news', args=[obj.pk])
            )
        return obj.get_status_display()
    approval_actions.short_description = 'Actions'

    def approve_news(self, request, queryset):
        queryset.update(
            status='APPROVED',
            approved_by=request.user,
            approved_at=timezone.now()
        )
    approve_news.short_description = "Approve selected news"

    def reject_news(self, request, queryset):
        queryset.update(status='REJECTED')
    reject_news.short_description = "Reject selected news"

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            if obj.status == 'APPROVED':
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
        super().save_model(request, obj, form, change)

    def get_urls(self):
        from django.urls import path
        urls = super().get_urls()
        custom_urls = [
            path(
                '<int:news_id>/approve/',
                self.admin_site.admin_view(self.approve_news_view),
                name='approve_news',
            ),
            path(
                '<int:news_id>/reject/',
                self.admin_site.admin_view(self.reject_news_view),
                name='reject_news',
            ),
        ]
        return custom_urls + urls

    def approve_news_view(self, request, news_id):
        from django.http import HttpResponseRedirect
        from django.contrib import messages
        news = self.model.objects.get(pk=news_id)
        news.status = 'APPROVED'
        news.approved_by = request.user
        news.approved_at = timezone.now()
        news.save()
        messages.success(request, f'"{news.title}" has been approved.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    def reject_news_view(self, request, news_id):
        from django.http import HttpResponseRedirect
        from django.contrib import messages
        news = self.model.objects.get(pk=news_id)
        news.status = 'REJECTED'
        news.save()
        messages.warning(request, f'"{news.title}" has been rejected.')
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

    class Media:
        css = {
            'all': (
                'admin/css/content-blocks.css',
                'admin/css/custom-admin.css',
            )
        }
        js = ('admin/js/content-blocks.js',)




@admin.register(DialogContent)
class DialogContentAdmin(admin.ModelAdmin):
    list_display = ('news', 'title')
    fields = ('news', 'title', 'body')