from django.contrib import admin
from django.utils.html import format_html
from .models import News, NewsCategory

@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'description')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}

@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    # Fields to display in the list view
    list_display = (
        'title',
        'category_display',
        'published_date',
        'author',
        'is_featured',
        'is_published',
        'image_preview'
    )

    # Fields that can be edited directly in the list view
    list_editable = ('is_featured', 'is_published')

    # Filters shown in the right sidebar
    list_filter = (
        'category',
        'is_featured',
        'is_published',
        'published_date',
        'author'
    )

    # Fields to search
    search_fields = (
        'title',
        'content',
        'author'
    )

    # Default ordering
    ordering = ('-published_date',)

    # Fields to automatically populate
    prepopulated_fields = {'slug': ('title',)}

    # Organize fields into fieldsets
    fieldsets = (
        ('Content', {
            'fields': ('title', 'slug', 'content', 'image')
        }),
        ('Category & Status', {
            'fields': ('category', 'is_featured', 'is_published')
        }),
        ('Author & Dates', {
            'fields': ('author',),
            'classes': ('collapse',)
        })
    )

    # Number of items per page
    list_per_page = 20

    # Add date hierarchy navigation
    date_hierarchy = 'published_date'

    # Custom display methods
    def category_display(self, obj):
        return format_html(
            '<span style="color: {};">{}</span>',
            '#1980e6',
            obj.category.name
        )
    category_display.short_description = 'Category'

    def image_preview(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" style="max-height: 50px; max-width: 100px;"/>',
                obj.image.url
            )
        return "No Image"
    image_preview.short_description = 'Image Preview'

    # Custom actions
    actions = ['make_published', 'make_unpublished', 'mark_as_featured', 'unmark_as_featured']

    def make_published(self, request, queryset):
        queryset.update(is_published=True)
    make_published.short_description = "Mark selected news as published"

    def make_unpublished(self, request, queryset):
        queryset.update(is_published=False)
    make_unpublished.short_description = "Mark selected news as unpublished"

    def mark_as_featured(self, request, queryset):
        queryset.update(is_featured=True)
    mark_as_featured.short_description = "Mark selected news as featured"

    def unmark_as_featured(self, request, queryset):
        queryset.update(is_featured=False)
    unmark_as_featured.short_description = "Unmark selected news as featured"

    # Add save message
    def save_model(self, request, obj, form, change):
        if not change:
            obj.author = request.user.get_full_name() or request.user.username
        super().save_model(request, obj, form, change)

    class Media:
        css = {
            'all': ('css/custom_admin.css',)
        }
