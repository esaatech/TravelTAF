import requests
import json
from typing import Optional, Dict, Any
from django.conf import settings
from ..config.settings import BASE_URL, ENDPOINTS
import logging

logger = logging.getLogger(__name__)

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

    @classmethod
    def query_document(cls, key: str, query: str, config: dict = None) -> dict:
        """
        Query a document using its key.
        """
        try:
            # Only log critical information
            logger.info(f"Querying document: {key}")
            
            base_url = cls.BASE_URL.rstrip('/')
            endpoint = f"{base_url}/documents/{key}/query"
            
            response = requests.post(
                endpoint,
                json={"query": query},
                headers={'Content-Type': 'application/json'},
                timeout=10
            )
            
            # Only log errors (minimal overhead during normal operation)
            if not response.ok:
                logger.error(f"API error: Status={response.status_code}, Response={response.text[:200]}")
            
            response.raise_for_status()
            return response.json()
            
        except Exception as e:
            logger.error(f"Error querying document {key}: {str(e)}", exc_info=True)
            raise
