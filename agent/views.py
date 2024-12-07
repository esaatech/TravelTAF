from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Interaction
from .serializers import MessageSerializer, ChatHistorySerializer
from .services.document_service import DocumentService
from .services.key_manager import KeyManager

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
        
        # Update the interaction with the response
        interaction.response = response
        interaction.status = 'processed'
        interaction.save()

    def process_message(self, message):
        """
        Process the incoming message by querying the uploaded documents.
        """
        try:
            # Get all document keys
            documents = KeyManager.list_all()
            
            if not documents:
                return "No documents are available to process your query. Please upload documents first."
            
            # Prepare the responses from all documents
            responses = []
            
            for filename, data in documents.items():
                try:
                    # Query each document using its key
                    doc_response = DocumentService.query_document(
                        key=data['key'],
                        query=message,
                        config=data.get('prompt_config', {})
                    )
                    
                    if doc_response and doc_response.get('response'):
                        if doc_response['response'] != "No relevant information found for your query.":
                            responses.append({
                                'filename': filename,
                                'response': doc_response['response'],
                                'confidence': doc_response.get('confidence', 1.0)
                            })
                except Exception as e:
                    print(f"Error querying document {filename}: {str(e)}")
                    continue
            
            if not responses:
                return "I couldn't find relevant information in the available documents. Please try rephrasing your question."
            
            # Sort responses by confidence if available
            responses.sort(key=lambda x: x.get('confidence', 0), reverse=True)
            
            # Format the response
            return self._format_responses(responses)
            
        except Exception as e:
            print(f"Error processing message: {str(e)}")
            return "I apologize, but I encountered an error processing your request. Please try again later."

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

        # Get the updated instance with the response
        instance = self.queryset.get(id=serializer.instance.id)
        response_serializer = self.get_serializer(instance)
        
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)


# Create your views here.
