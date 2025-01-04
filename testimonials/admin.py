from django.contrib import admin
from .models import Testimonial

@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'testimonial_type', 'location', 'rating', 'duration', 'is_active')
    list_filter = ('testimonial_type', 'rating', 'is_active')
    search_fields = ('name', 'location', 'testimonial_text')
    readonly_fields = ('created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'initials', 'location')
        }),
        ('Testimonial Details', {
            'fields': ('rating', 'testimonial_text', 'testimonial_type', 'duration')
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )
    list_editable = ('is_active',)
