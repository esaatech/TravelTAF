from django.contrib import admin
from .models import Promotion

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ('title', 'link_type', 'is_active', 'order', 'start_date', 'end_date')
    list_filter = ('is_active', 'link_type')
    search_fields = ('title', 'description')
    ordering = ('order', '-start_date')
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'description', 'image')
        }),
        ('Link Settings', {
            'fields': ('link_type', 'external_url', 'internal_name')
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order', 'start_date', 'end_date')
        }),
    )

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['internal_name'].help_text = (
            "Enter the URL name from your urls.py (e.g., 'tools:detail')"
        )
        return form
