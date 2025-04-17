from django.contrib import admin
from .models import TravelDestination, VacationSearch
from adminsortable2.admin import SortableAdminMixin

class TravelDestinationAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'code', 'is_active', 'is_featured', 'order']
    list_editable = ['is_active', 'is_featured']
    list_filter = ['is_active', 'is_featured']
    search_fields = ['name', 'code']
    ordering = ['order', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'code', 'flag', 'is_active', 'is_featured')
        }),
        ('Features', {
            'fields': (
                ('feature1_icon', 'feature1_text'),
                ('feature2_icon', 'feature2_text'),
                ('feature3_icon', 'feature3_text'),
            )
        }),
    )
    
    def get_readonly_fields(self, request, obj=None):
        if obj:  # Editing an existing object
            return ('code',)  # Make code field readonly after creation
        return ()

# Register your models here
admin.site.register(TravelDestination, TravelDestinationAdmin)
admin.site.register(VacationSearch)
