import requests
import json
from typing import Optional, Dict, Any
from django.conf import settings

class DocumentService:
    """Service for handling document operations with the RAG Chatbot API."""
    
    BASE_URL = "https://rag-chatbot-api-578103433472.us-central1.run.app"
    
    @classmethod
    def upload_document(cls, file, prompt_config: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Upload a document to the API.
        Returns the response containing the document key.
        """
        endpoint = f"{cls.BASE_URL}/documents/upload"
        
        # Prepare the multipart form data
        files = {'file': file}
        data = {}
        if prompt_config:
            data['prompt_config'] = json.dumps(prompt_config)
            
        response = requests.post(endpoint, files=files, data=data)
        response.raise_for_status()
        return response.json()

    @classmethod
    def update_document(cls, key: str, file=None, prompt_config: Optional[Dict] = None) -> Dict[str, Any]:
        """Update an existing document or its configuration."""
        if file:
            # Full document update
            endpoint = f"{cls.BASE_URL}/documents/{key}/update"
            files = {'file': file}
            data = {}
            if prompt_config:
                data['prompt_config'] = json.dumps(prompt_config)
            response = requests.put(endpoint, files=files, data=data)
        else:
            # Config-only update
            endpoint = f"{cls.BASE_URL}/documents/{key}/update-config"
            response = requests.put(endpoint, json={'prompt_config': prompt_config})
            
        response.raise_for_status()
        return response.json()

    @classmethod
    def delete_document(cls, key: str) -> bool:
        """Delete a document from the API."""
        endpoint = f"{cls.BASE_URL}/documents/{key}"
        response = requests.delete(endpoint)
        response.raise_for_status()
        return True
