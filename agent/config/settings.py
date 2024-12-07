BASE_URL = "https://rag-chatbot-api-578103433472.us-central1.run.app/"
ENDPOINTS = {
    'upload': '/documents/upload',
    'query': '/documents/{key}/query',
    'update': '/documents/{key}/update',
    'update_config': '/documents/{key}/update-config',
    'delete': '/documents/{key}'
}
KEY_FILE_PATH = 'path/to/keys.txt'
