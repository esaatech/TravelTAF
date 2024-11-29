from rest_framework import serializers
from .models import Interaction

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'message', 'response', 'status', 'created_at']
        read_only_fields = ['id', 'response', 'status', 'created_at']

class ChatHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Interaction
        fields = ['id', 'message', 'response', 'status', 'created_at']