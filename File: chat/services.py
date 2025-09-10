from django.contrib.auth import get_user_model
from django.db import transaction
from django.utils import timezone
from channels.db import database_sync_to_async
from .models import ChatRoom, ChatMessage, ChatSession
from .serializers import ChatMessageSerializer, ChatRoomSerializer

User = get_user_model()


class ChatService:
    """Business logic for chat operations"""

    @staticmethod
    def create_room(name, description, creator, participant_ids=None):
        """Create a new chat room with participants"""
        with transaction.atomic():
            room = ChatRoom.objects.create(
                name=name,
                description=description
            )
            room.participants.add(creator)
            
            if participant_ids:
                participants = User.objects.filter(id__in=participant_ids)
                room.participants.add(*participants)
            
            return room

    @staticmethod
    def send_message(room_id, sender, content, message_type='text'):
        """Send a message to a chat room"""
        try:
            room = ChatRoom.objects.get(id=room_id)
            if sender not in room.participants.all():
                raise ValueError("User is not a participant in this room")
            
            message = ChatMessage.objects.create(
                room=room,
                sender=sender,
                content=content,
                message_type=message_type
            )
            
            # Update room's updated_at timestamp
            room.save()
            
            return message
        except ChatRoom.DoesNotExist:
            raise ValueError("Chat room not found")

    @staticmethod
    def get_room_messages(room_id, user, limit=50, offset=0):
        """Get messages for a room with pagination"""
        try:
            room = ChatRoom.objects.get(id=room_id)
            if user not in room.participants.all():
                raise ValueError("User is not a participant in this room")
            
            messages = room.messages.filter(
                is_deleted=False
            ).select_related('sender')[offset:offset + limit]
            
            return messages
        except ChatRoom.DoesNotExist:
            raise ValueError("Chat room not found")

    @staticmethod
    def create_session(user, room, channel_name):
        """Create or update a chat session"""
        session, created = ChatSession.objects.update_or_create(
            user=user,
            room=room,
            defaults={
                'channel_name': channel_name,
                'is_active': True,
                'last_seen': timezone.now()
            }
        )
        return session

    @staticmethod
    def close_session(channel_name):
        """Close a chat session"""
        try:
            session = ChatSession.objects.get(channel_name=channel_name)
            session.is_active = False
            session.save()
            return session
        except ChatSession.DoesNotExist:
            pass

    @staticmethod
    @database_sync_to_async
    def async_send_message(room_id, sender, content, message_type='text'):
        """Async version of send_message for WebSocket consumers"""
        return ChatService.send_message(room_id, sender, content, message_type)

    @staticmethod
    @database_sync_to_async
    def async_create_session(user, room, channel_name):
        """Async version of create_session"""
        return ChatService.create_session(user, room, channel_name)

    @staticmethod
    @database_sync_to_async
    def async_close_session(channel_name):
        """Async version of close_session"""
        return ChatService.close_session(channel_name)

    @staticmethod
    @database_sync_to_async
    def async_get_room(room_id):
        """Get room asynchronously"""
        try:
            return ChatRoom.objects.get(id=room_id)
        except ChatRoom.DoesNotExist:
            return None