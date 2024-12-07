import requests
import json
from typing import Optional, Dict, Any
from django.conf import settings
from ..config.settings import BASE_URL, ENDPOINTS

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
        
        Args:
            key: The document's API key
            query: The user's question
            config: Optional configuration for response formatting
            
        Returns:
            dict containing the response and any additional metadata
        """
        try:
            # Construct the endpoint URL
            endpoint = BASE_URL + ENDPOINTS['query'].format(key=key)
            
            # Prepare the payload
            payload = {
                "query": query
            }
            
            # Add configuration if provided
            if config:
                payload.update(config)
            
            # Make the API request
            response = requests.post(
                endpoint,
                json=payload
            )
            
            # Check for successful response
            response.raise_for_status()
            
            # Parse and return the response
            data = response.json()
            
            if 'response' in data:
                return {
                    "response": data['response'],
                    "confidence": data.get('confidence', 1.0)
                }
            
            return {
                "response": "No relevant information found for your query.",
                "confidence": 0
            }
            
        except requests.exceptions.RequestException as e:
            print(f"API request error: {str(e)}")
            raise Exception(f"Error querying document: {str(e)}")
        except Exception as e:
            print(f"General error: {str(e)}")
            raise Exception(f"Error processing query: {str(e)}")
