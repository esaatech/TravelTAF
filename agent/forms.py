from django import forms

class DocumentForm(forms.Form):
    """Form for handling document uploads and updates."""
    file = forms.FileField(required=False)
    
    # Configuration fields
    company_name = forms.CharField(required=False)
    agent_role = forms.CharField(required=False)
    response_style = forms.CharField(required=False)
    tone = forms.CharField(required=False)
    
    def clean(self):
        cleaned_data = super().clean()
        file = cleaned_data.get('file')
        
        # Validate file type if provided
        if file:
            valid_extensions = ['.txt', '.pdf', '.docx', '.csv']
            ext = str(file.name).lower().split('.')[-1]
            if f'.{ext}' not in valid_extensions:
                raise forms.ValidationError(
                    f"Unsupported file type. Allowed: {', '.join(valid_extensions)}"
                )
        
        # Ensure at least file or one config field is provided
        config_fields = ['company_name', 'agent_role', 'response_style', 'tone']
        if not file and not any(cleaned_data.get(field) for field in config_fields):
            raise forms.ValidationError(
                "Either a file or configuration updates must be provided."
            )
        
        return cleaned_data