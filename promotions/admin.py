from django.contrib import admin
from .models import Promotion, PromotionType

@admin.register(PromotionType)
class PromotionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'is_active', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_filter = ['is_active']

@admin.register(Promotion)
class PromotionAdmin(admin.ModelAdmin):
    list_display = ['title', 'promotion_type', 'is_active', 'start_date', 'end_date', 'order']
    list_filter = ['promotion_type', 'is_active', 'start_date', 'end_date']
    search_fields = ['title', 'description', 'internal_name']
    ordering = ['order', '-start_date']
    
    fieldsets = (
        (None, {
            'fields': ('title', 'description', 'promotion_type')
        }),
        ('Image', {
            'fields': ('image',)
        }),
        ('Link Settings', {
            'fields': ('link_type', 'external_url', 'internal_name', 'cta_text'),
            'description': 'Configure link and call-to-action button'
        }),
        ('Display Settings', {
            'fields': ('is_active', 'order', 'start_date', 'end_date'),
            'description': 'Control when and how the promotion appears'
        })
    )
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields['end_date'].help_text = 'Leave blank for no end date'
        return form

