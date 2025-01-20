from django.contrib import admin
from .models import School, ProgramLevel, FieldOfStudy, Country, Countries, VisaType, VisaRelationship

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

from django.contrib import admin
from .models import StudyServicePlan, StudyPlanFeature, StudyPlanService

class StudyPlanFeatureInline(admin.TabularInline):
    model = StudyPlanFeature
    extra = 1
    ordering = ['order']
    fields = ['feature', 'is_highlighted', 'order']

class StudyPlanServiceInline(admin.TabularInline):
    model = StudyPlanService
    extra = 1
    ordering = ['order']
    fields = ['service', 'is_highlighted', 'order']

@admin.register(StudyServicePlan)
class StudyServicePlanAdmin(admin.ModelAdmin):
    list_display = ['name', 'plan_type', 'price', 'timeline', 'is_active', 'order']
    list_editable = ['order', 'is_active']
    list_filter = ['plan_type', 'is_active']
    search_fields = ['name', 'description']
    inlines = [StudyPlanFeatureInline, StudyPlanServiceInline]
    fieldsets = (
        (None, {
            'fields': ('name', 'plan_type', 'description')
        }),
        ('Pricing & Timeline', {
            'fields': ('price', 'timeline')
        }),
        ('Button Configuration', {
            'fields': ('button_text', 'button_url')
        }),
        ('Settings', {
            'fields': ('is_active', 'order')
        })
    )

@admin.register(Countries)
class CountriesAdmin(admin.ModelAdmin):
    list_display = ('name', 'iso_code_2', 'iso_code_3', 'region', 'continent', 'created_at', 'updated_at')
    search_fields = ('name', 'iso_code_2', 'iso_code_3')
    list_filter = ('region', 'continent')

@admin.register(VisaType)
class VisaTypeAdmin(admin.ModelAdmin):
    list_display = ['name']
    search_fields = ['name']
    ordering = ['name']

@admin.register(VisaRelationship)
class VisaRelationshipAdmin(admin.ModelAdmin):
    list_display = [
        'citizenship_country', 
        'destination_country', 
        'visa_type',
        'is_visa_free',
        'is_eta',
        'is_active'
    ]
    list_filter = [
        'is_visa_free',
        'is_eta',
        'is_active',
        'citizenship_country',
        'destination_country'
    ]
    search_fields = [
        'citizenship_country__name',
        'destination_country__name',
        'visa_type__name'
    ]