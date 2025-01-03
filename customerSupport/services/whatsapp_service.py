import requests
from django.conf import settings

class WhatsAppService:
    def __init__(self):
        self.base_url = "https://graph.facebook.com/v17.0"
        self.phone_number_id = settings.WHATSAPP_PHONE_ID
        self.access_token = settings.WHATSAPP_ACCESS_TOKEN
        
    def send_message(self, to_number, message):
        endpoint = f"{self.base_url}/{self.phone_number_id}/messages"
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json"
        }
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": message}
        }
        return requests.post(endpoint, json=payload, headers=headers)