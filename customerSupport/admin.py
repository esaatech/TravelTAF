from django.contrib import admin
from .models import WhatsAppConversation, WhatsAppMessage, WhatsAppQuickReply
from django.utils.html import format_html

@admin.register(WhatsAppMessage)
class WhatsAppMessageAdmin(admin.ModelAdmin):
    list_display = ['conversation', 'direction', 'content_preview', 'status', 'timestamp']
    list_filter = ['direction', 'status', 'timestamp', 'processed']
    search_fields = ['content', 'conversation__customer_name', 'conversation__customer_phone']
    readonly_fields = ['message_id', 'timestamp']

    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content

@admin.register(WhatsAppConversation)
class WhatsAppConversationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'customer_phone', 'status', 'assigned_to', 'updated_at']
    list_filter = ['status', 'assigned_to', 'created_at']
    search_fields = ['customer_name', 'customer_phone']
    readonly_fields = ['created_at', 'updated_at']
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if not request.user.is_superuser:
            qs = qs.filter(assigned_to=request.user)
        return qs

@admin.register(WhatsAppQuickReply)
class WhatsAppQuickReplyAdmin(admin.ModelAdmin):
    list_display = ['title', 'content_preview', 'created_by', 'updated_at']
    search_fields = ['title', 'content']
    
    def content_preview(self, obj):
        return obj.content[:50] + '...' if len(obj.content) > 50 else obj.content
