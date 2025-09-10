from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import ChatRoom, ChatMessage, ChatSession

User = get_user_model()


class UserBasicSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ChatMessageSerializer(serializers.ModelSerializer):
    sender = UserBasicSerializer(read_only=True)
    
    class Meta:
        model = ChatMessage
        fields = [
            'id', 'content', 'message_type', 'sender', 
            'created_at', 'edited_at', 'is_deleted'
        ]
        read_only_fields = ['id', 'sender', 'created_at', 'edited_at']

    def create(self, validated_data):
        validated_data['sender'] = self.context['request'].user
        return super().create(validated_data)


class ChatRoomSerializer(serializers.ModelSerializer):
    participants = UserBasicSerializer(many=True, read_only=True)
    participant_ids = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )
    message_count = serializers.SerializerMethodField()
    last_message = serializers.SerializerMethodField()

    class Meta:
        model = ChatRoom
        fields = [
            'id', 'name', 'description', 'participants', 'participant_ids',
            'created_at', 'updated_at', 'is_active', 'message_count', 'last_message'
        ]
        read_only_fields = ['id', 'created_at', 'updated_at']

    def get_message_count(self, obj):
        return obj.messages.filter(is_deleted=False).count()

    def get_last_message(self, obj):
        last_msg = obj.messages.filter(is_deleted=False).last()
        if last_msg:
            return ChatMessageSerializer(last_msg).data
        return None

    def create(self, validated_data):
        participant_ids = validated_data.pop('participant_ids', [])
        room = super().create(validated_data)
        
        # Add creator as participant
        room.participants.add(self.context['request'].user)
        
        # Add specified participants
        if participant_ids:
            users = User.objects.filter(id__in=participant_ids)
            room.participants.add(*users)
        
        return room


class ChatSessionSerializer(serializers.ModelSerializer):
    user = UserBasicSerializer(read_only=True)
    room = ChatRoomSerializer(read_only=True)

    class Meta:
        model = ChatSession
        fields = ['id', 'user', 'room', 'connected_at', 'last_seen', 'is_active']