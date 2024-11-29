from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from .models import Interaction
from .serializers import MessageSerializer, ChatHistorySerializer

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
        Process the incoming message and generate a response.
        This is where you'd add your chatbot logic.
        """
        # For now, return a simple response
        return f"Thank you for your message: '{message}'. Our team will respond shortly."

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
