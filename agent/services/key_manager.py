import json
import os
from typing import Dict, Optional
from django.conf import settings

class KeyManager:
    """Manages document keys and configurations in a JSON file."""
    
    # Path to the JSON file storing keys and configurations
    KEY_FILE = os.path.join(settings.BASE_DIR, 'document_keys.json')
    
    @classmethod
    def _ensure_file_exists(cls) -> None:
        """Ensure the key file exists and is properly initialized."""
        if not os.path.exists(cls.KEY_FILE):
            with open(cls.KEY_FILE, 'w') as f:
                json.dump({}, f)

    @classmethod
    def _read_keys(cls) -> Dict:
        """Read all keys from the file."""
        cls._ensure_file_exists()
        try:
            with open(cls.KEY_FILE, 'r') as f:
                return json.load(f)
        except json.JSONDecodeError:
            return {}

    @classmethod
    def _write_keys(cls, data: Dict) -> None:
        """Write keys to the file."""
        with open(cls.KEY_FILE, 'w') as f:
            json.dump(data, f, indent=2)

    @classmethod
    def save_key(cls, filename: str, key: str, prompt_config: Optional[Dict] = None) -> None:
        """
        Save a document key and its configuration.
        
        Args:
            filename: Name of the uploaded file
            key: API key returned from the document service
            prompt_config: Optional configuration for the document
        """
        data = cls._read_keys()
        data[filename] = {
            'key': key,
            'prompt_config': prompt_config or {}
        }
        cls._write_keys(data)

    @classmethod
    def get_key(cls, filename: str) -> Optional[Dict]:
        """
        Get a document's key and configuration by filename.
        
        Args:
            filename: Name of the file
            
        Returns:
            Dict containing key and configuration or None if not found
        """
        data = cls._read_keys()
        return data.get(filename)

    @classmethod
    def get_key_by_value(cls, key: str) -> Optional[Dict]:
        """
        Get document data by key value.
        
        Args:
            key: The API key to search for
            
        Returns:
            Dict containing filename and configuration or None if not found
        """
        data = cls._read_keys()
        for filename, file_data in data.items():
            if file_data.get('key') == key:
                return {'filename': filename, **file_data}
        return None

    @classmethod
    def update_key(cls, old_key: str, new_key: str, prompt_config: dict, new_filename: str = None) -> bool:
        """
        Update a document's key and configuration.
        
        Args:
            old_key: Current API key
            new_key: New API key (can be same as old_key if only updating config)
            prompt_config: New configuration
            new_filename: Optional new filename
            
        Returns:
            bool indicating success
        """
        data = cls._read_keys()
        for filename, file_data in data.items():
            if file_data.get('key') == old_key:
                if new_filename and new_filename != filename:
                    # Create new entry with new filename
                    data[new_filename] = {
                        'key': new_key,
                        'prompt_config': prompt_config
                    }
                    # Delete old entry
                    del data[filename]
                else:
                    # Update existing entry
                    data[filename] = {
                        'key': new_key,
                        'prompt_config': prompt_config
                    }
                cls._write_keys(data)
                return True
        return False

    @classmethod
    def delete_key_by_value(cls, key: str) -> bool:
        """
        Delete a document's key by its value.
        
        Args:
            key: The API key to delete
            
        Returns:
            bool indicating success
        """
        data = cls._read_keys()
        for filename, file_data in data.items():
            if file_data.get('key') == key:
                del data[filename]
                cls._write_keys(data)
                return True
        return False

    @classmethod
    def list_all(cls) -> Dict:
        """
        List all stored documents and their configurations.
        
        Returns:
            Dict of all stored documents
        """
        return cls._read_keys()
