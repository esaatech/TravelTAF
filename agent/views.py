from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Interaction
from .serializers import MessageSerializer, ChatHistorySerializer
from .services.document_service import DocumentService
from .services.key_manager import KeyManager
import requests
import uuid
import json

class ChatViewSet(viewsets.ModelViewSet):
    queryset = Interaction.objects.filter(type='chat')
    serializer_class = MessageSerializer

    def get_queryset(self):
        # If user is authenticated, return their chat history
        if self.request.user.is_authenticated:
            return self.queryset.filter(user=self.request.user)
        # For anonymous users, return empty queryset
        return self.queryset.none()

    def perform_create(self, serializer):
        # Create the interaction
        interaction = serializer.save(
            user=self.request.user if self.request.user.is_authenticated else None,
            type='chat',
            status='pending'
        )

        # Process the message and generate response
        response = self.process_message(interaction.message)
        
        # Store as JSON string
        interaction.response = json.dumps(response)
        interaction.status = 'processed'
        interaction.save()

    def process_message(self, message):
        """
        Process the incoming message by sending it to n8n webhook.
        """
        try:
            # n8n webhook URL
            base_url = "https://38d1-147-194-133-23.ngrok-free.app"
            n8n_webhook_url = f"{base_url}/webhook/9d50356f-f1b4-469f-adc6-64a8a84102ad"
            
            # Get session ID from request
            session_id = self.request.session.get('chat_session_id')
            
            if not session_id:
                session_id = f"user-{uuid.uuid4().hex[:8]}"
                self.request.session['chat_session_id'] = session_id
            
            # Prepare the payload
            payload = {
                "chatInput": message,
                "sessionId": session_id
            }
            
            # Make request to n8n webhook
            response = requests.post(
                n8n_webhook_url,
                json=payload,
                headers={
                    "Content-Type": "application/json"
                }
            )
            
            if response.status_code == 200:
                response_data = response.json()
                if isinstance(response_data, dict) and 'output' in response_data:
                    # Parse the nested JSON string
                    try:
                        parsed_output = json.loads(response_data['output'])
                        return {
                            'message': parsed_output['output'],
                            'show_button': parsed_output['button'] == 'yes'
                        }
                    except json.JSONDecodeError:
                        return {
                            'message': response_data['output'],
                            'show_button': False
                        }
                return {
                    'message': "Received response from server but in unexpected format",
                    'show_button': False
                }
            else:
                return {
                    'message': "Error processing your request. Please try again later.",
                    'show_button': False
                }
                
        except Exception as e:
            return {
                'message': "I apologize, but I encountered an error processing your request. Please try again later.",
                'show_button': False
            }

    def _format_responses(self, responses):
        """
        Format multiple document responses into a coherent response.
        """
        if len(responses) == 1:
            # Single document response
            return responses[0]['response']
        
        # Multiple document responses
        formatted = "I found relevant information in multiple documents:\n\n"
        for resp in responses:
            formatted += f"From {resp['filename']} (confidence: {resp['confidence']:.2f}):\n{resp['response']}\n\n"
        
        return formatted.strip()

    @action(detail=False, methods=['get'])
    def history(self, request):
        """Get chat history for the current user"""
        queryset = self.get_queryset()
        serializer = ChatHistorySerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        instance = self.queryset.get(id=serializer.instance.id)
        import json
        response_data = json.loads(instance.response)
        return Response({
            "id": instance.id,
            "message": instance.message,
            "status": instance.status,
            "created_at": instance.created_at,
            "message": response_data.get("message", ""),
            "show_button": response_data.get("show_button", False)
        }, status=status.HTTP_201_CREATED)


# Create your views here.
