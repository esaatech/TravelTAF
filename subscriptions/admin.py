from django.contrib import admin
from django.utils.html import format_html
from .models import FeatureCatalog, SubscriptionPlan, UserSubscription

@admin.register(FeatureCatalog)
class FeatureCatalogAdmin(admin.ModelAdmin):
    """
    Admin interface for managing features/tools catalog.
    """
    list_display = ['name', 'identifier', 'type', 'is_active']
    list_filter = ['type', 'is_active']
    search_fields = ['name', 'identifier', 'description']
    prepopulated_fields = {'identifier': ('name',)}
    ordering = ['type', 'name']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'identifier', 'type')
        }),
        ('Details', {
            'fields': ('description', 'is_active')
        }),
    )


@admin.register(SubscriptionPlan)
class SubscriptionPlanAdmin(admin.ModelAdmin):
    """
    Admin interface for managing subscription plans.
    """
    list_display = [
        'name', 
        'price_display', 
        'duration_type', 
        'has_full_access',
        'feature_count', 
        'is_active'
    ]
    list_filter = ['duration_type', 'has_full_access', 'is_active']
    search_fields = ['name', 'description']
    filter_horizontal = ['features']
    
    fieldsets = (
        (None, {
            'fields': ('name', 'description')
        }),
        ('Pricing & Duration', {
            'fields': ('price', 'duration_type')
        }),
        ('Access Control', {
            'fields': ('has_full_access', 'is_active')
        }),
        ('Features', {
            'fields': ('features',),
            'classes': ('wide',)
        }),
        ('Stripe Integration', {
            'fields': ('stripe_price_id',),
            'classes': ('collapse',)
        }),
    )

    def price_display(self, obj):
        """Format price display with currency."""
        return f"${obj.price}"  # Simple string formatting
    price_display.short_description = 'Price'

    def feature_count(self, obj):
        """Display count of features in the plan."""
        return obj.features.count()
    feature_count.short_description = 'Features'

    def get_form(self, request, obj=None, **kwargs):
        """
        Override get_form to save features temporarily
        """
        if request.method == 'POST':
            request._features_data = request.POST.getlist('features')
        return super().get_form(request, obj, **kwargs)

    def save_model(self, request, obj, form, change):
        """
        First save the model, then handle the features
        """
        super().save_model(request, obj, form, change)
        # Now that we have an ID, we can handle the features
        if hasattr(request, '_features_data'):
            obj.features.clear()
            obj.features.add(*request._features_data)


@admin.register(UserSubscription)
class UserSubscriptionAdmin(admin.ModelAdmin):
    """
    Admin interface for managing user subscriptions.
    """
    list_display = [
        'user', 
        'plan', 
        'status', 
        'subscription_period',
        'is_currently_active'
    ]
    list_filter = ['status', 'plan', 'start_date']
    search_fields = [
        'user__username', 
        'user__email', 
        'plan__name',
        'stripe_subscription_id'
    ]
    raw_id_fields = ['user']
    
    fieldsets = (
        (None, {
            'fields': ('user', 'plan', 'status')
        }),
        ('Subscription Period', {
            'fields': ('start_date', 'end_date')
        }),
        ('Stripe Details', {
            'fields': ('stripe_subscription_id',),
            'classes': ('collapse',)
        }),
        ('Status', {
            'fields': ('is_active',)
        }),
    )
    readonly_fields = ['is_currently_active']

    def subscription_period(self, obj):
        """Display subscription period in a readable format."""
        if obj.end_date:
            return format_html(
                '{} to {}',
                obj.start_date.strftime('%Y-%m-%d'),
                obj.end_date.strftime('%Y-%m-%d')
            )
        return format_html(
            'From {}',
            obj.start_date.strftime('%Y-%m-%d')
        )
    subscription_period.short_description = 'Period'

    def is_currently_active(self, obj):
        """Display if subscription is currently active."""
        return obj.is_active
    is_currently_active.boolean = True
    is_currently_active.short_description = 'Active'


# Optional: Register models in a custom admin site
class SubscriptionAdminSite(admin.AdminSite):
    site_header = 'Subscription Management'
    site_title = 'Subscription Admin'
    index_title = 'Subscription Administration'

# subscription_admin_site = SubscriptionAdminSite(name='subscription_admin')
# subscription_admin_site.register(FeatureCatalog, FeatureCatalogAdmin)
# subscription_admin_site.register(SubscriptionPlan, SubscriptionPlanAdmin)
# subscription_admin_site.register(UserSubscription, UserSubscriptionAdmin)
