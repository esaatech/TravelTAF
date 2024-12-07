from django.contrib import admin
from django.http import HttpResponseRedirect
from django.urls import path
from django.shortcuts import render
from django.contrib import messages
from .models import Interaction, DocumentManagement
from .forms import DocumentForm
from .services.document_service import DocumentService
from .services.key_manager import KeyManager
from django.template.loader import get_template
from django.template import TemplateDoesNotExist
from django.urls import reverse
@admin.register(Interaction)
class InteractionAdmin(admin.ModelAdmin):
    """Admin interface for managing user interactions."""
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
        return obj.get_duration()
    get_duration.short_description = 'Duration'

@admin.register(DocumentManagement)
class DocumentManagementAdmin(admin.ModelAdmin):
    """Admin interface for document management."""
    
    change_list_template = 'admin/document_management/change_list.html'
    
    def has_add_permission(self, request):
        """Disable add permission as this is just a placeholder."""
        return False
    
    def has_delete_permission(self, request, obj=None):
        """Disable delete permission as this is just a placeholder."""
        return False
    
    def has_change_permission(self, request, obj=None):
        """Disable change permission as this is just a placeholder."""
        return False

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('upload/', self.upload_document, name='document-upload'),
            path('update/<str:key>/', self.update_document, name='document-update'),
            path('delete/<str:key>/', self.delete_document, name='document-delete'),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        try:
            template = get_template(self.change_list_template)
            print("Template found:", template.origin.name)
        except TemplateDoesNotExist:
            print("Template not found:", self.change_list_template)
        
        extra_context = extra_context or {}
        extra_context['documents'] = KeyManager.list_all()
        return super().changelist_view(request, extra_context)

    def upload_document(self, request):
        """Handle document upload."""
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    file = form.cleaned_data['file']
                    config = {k: v for k, v in form.cleaned_data.items() if v and k != 'file'}
                    
                    response = DocumentService.upload_document(file, config)
                    KeyManager.save_key(file.name, response['key'], config)
                    
                    messages.success(request, f"Document uploaded successfully. Key: {response['key']}")
                    return HttpResponseRedirect('../')
                except Exception as e:
                    messages.error(request, f"Error uploading document: {str(e)}")
        else:
            form = DocumentForm()
            
        context = {
            'form': form,
            'title': 'Upload Document',
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/document_management/upload_form.html', context)

    def update_document(self, request, key):
        """Handle document update."""
        document_data = KeyManager.get_key_by_value(key)
        if not document_data:
            messages.error(request, "Document not found")
            return HttpResponseRedirect('../')
            
        if request.method == 'POST':
            form = DocumentForm(request.POST, request.FILES)
            if form.is_valid():
                try:
                    file = form.cleaned_data.get('file')
                    config = {k: v for k, v in form.cleaned_data.items() if v and k != 'file'}
                    
                    response = DocumentService.update_document(key=key, file=file, prompt_config=config)
                    if response.get('new_key'):
                        KeyManager.update_key(key, response['new_key'], config)
                        
                    messages.success(request, "Document updated successfully")
                    return HttpResponseRedirect('../')
                except Exception as e:
                    messages.error(request, f"Error updating document: {str(e)}")
        else:
            form = DocumentForm(initial=document_data.get('prompt_config', {}))
            
        context = {
            'form': form,
            'title': 'Update Document',
            'key': key,
            **self.admin_site.each_context(request),
        }
        return render(request, 'admin/document_management/update_form.html', context)

    def delete_document(self, request, key):
        """Handle document deletion."""
        if request.method == 'POST':
            try:
                DocumentService.delete_document(key)
                KeyManager.delete_key_by_value(key)
                messages.success(request, "Document deleted successfully")
            except Exception as e:
                messages.error(request, f"Error deleting document: {str(e)}")
        return HttpResponseRedirect(
            reverse('admin:agent_documentmanagement_changelist')
        )




