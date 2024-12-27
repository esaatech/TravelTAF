from django.contrib import admin
from .models import School, ProgramLevel, FieldOfStudy, Country

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name', 'code')
    search_fields = ('name', 'code')
    ordering = ('name',)

@admin.register(ProgramLevel)
class ProgramLevelAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')

@admin.register(FieldOfStudy)
class FieldOfStudyAdmin(admin.ModelAdmin):
    list_display = ('name', 'value')
    search_fields = ('name', 'value')

@admin.register(School)
class SchoolAdmin(admin.ModelAdmin):
    list_display = ('name', 'country', 'tuition', 'scholarships_available', 
                   'work_opportunities', 'housing_available')
    list_filter = ('country', 'programs', 'fields_of_study', 
                  'scholarships_available', 'work_opportunities', 'housing_available')
    search_fields = ('name', 'location')
    filter_horizontal = ('programs', 'fields_of_study')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'location', 'country', 'logo', 'website', 'ranking', 'tuition')
        }),
        ('Programs & Fields', {
            'fields': ('programs', 'fields_of_study')
        }),
        ('Features', {
            'fields': ('scholarships_available', 'work_opportunities', 'housing_available')
        }),
    )

    actions = ['enable_all_features', 'disable_all_features']

    def enable_all_features(self, request, queryset):
        queryset.update(
            scholarships_available=True,
            work_opportunities=True,
            housing_available=True
        )
    enable_all_features.short_description = "Enable all features for selected schools"

    def disable_all_features(self, request, queryset):
        queryset.update(
            scholarships_available=False,
            work_opportunities=False,
            housing_available=False
        )
    disable_all_features.short_description = "Disable all features for selected schools"
