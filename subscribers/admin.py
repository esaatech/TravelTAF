from django.contrib import admin
from .models import Subscriber

@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscription_type', 'is_active', 'created_at')
    list_filter = ('subscription_type', 'is_active', 'created_at')
    search_fields = ('email',)
    date_hierarchy = 'created_at'