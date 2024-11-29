from django.contrib import admin
from .models import Interaction

@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing user interactions.
    Provides filtering, searching, and display options for monitoring interactions.
    """
    
    list_display = ('type', 'user', 'status', 'created_at', 'get_duration')
    list_filter = ('type', 'status', 'created_at')
    search_fields = ('message', 'response', 'user__username')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('user', 'type', 'status')
        }),
        ('Content', {
            'fields': ('message', 'response')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def get_duration(self, obj):
        """Calculate interaction duration"""
        return obj.get_duration()
    get_duration.short_description = 'Duration'
