from django.contrib import admin
from django.utils import timezone
from .models import ImmigrationProgram

@admin.register(ImmigrationProgram)
class ImmigrationProgramAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'status', 'featured', 'deadline', 'created_at')
    list_filter = ('status', 'featured', 'country', 'created_at')
    search_fields = ('name', 'country__name', 'description')
    readonly_fields = ('created_at', 'updated_at', 'approved_at', 'slug')
    list_editable = ('status', 'featured')
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'country'),
            'classes': ('wide',)
        }),
        ('Content', {
            'fields': ('description', 'eligibility_criteria', 'benefits', 'application_process'),
            'classes': ('wide', 'extrapretty')
        }),
        ('Program Details', {
            'fields': ('deadline', 'official_link'),
            'classes': ('wide',)
        }),
        ('Media', {
            'fields': ('featured_image',)
        }),
        ('Settings', {
            'fields': ('chat_enabled', 'featured')
        }),
        ('Status', {
            'fields': ('status', 'approved_by', 'approved_at', 'review_notes')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        })
    )

    def save_model(self, request, obj, form, change):
        if 'status' in form.changed_data:
            if obj.status == 'APPROVED':
                obj.approved_by = request.user
                obj.approved_at = timezone.now()
            else:
                obj.approved_by = None
                obj.approved_at = None
        super().save_model(request, obj, form, change)

    def get_queryset(self, request):
        return super().get_queryset(request).select_related('country', 'approved_by')
