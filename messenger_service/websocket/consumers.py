import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser

from chats.models import Chat
from chat_messages.models import Message, MessageStatus

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.user = self.scope["user"]

        if isinstance(self.user, AnonymousUser):
            await self.close()
            return

        self.chat_id = self.scope["url_route"]["kwargs"]["chat_id"]
        self.group_name = f"chat_{self.chat_id}"

        if not await self.user_in_chat():
            await self.close()
            return

        await self.channel_layer.group_add(
            self.group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        event_type = data.get("type")

        if event_type == "message":
            await self.handle_message(data)
        elif event_type == "typing":
            await self.handle_typing()
        elif event_type == "read":
            await self.handle_read(data)

    async def handle_message(self, data):
        text = data.get("text")
        message = await self.create_message(text)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.message",
                "message_id": message.id,
                "text": message.text,
                "user_id": message.sender_id,
                "username": self.user.username,
                "created_at": str(message.created_at)
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            "type": "message",
            "messageId": event["message_id"],
            "text": event["text"],
            "userId": event["user_id"],
            "username": event["username"],
            "createdAt": event["created_at"]
        }))

    async def handle_typing(self):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.typing",
                "user_id": self.user.id,
                "username": self.user.username
            }
        )

    async def chat_typing(self, event):
        await self.send(text_data=json.dumps({
            "type": "typing",
            "userId": event["user_id"],
            "username": event["username"]
        }))

    async def handle_read(self, data):
        message_id = data.get("message_id")
        await self.mark_as_read(message_id)

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "chat.read",
                "message_id": message_id,
                "user_id": self.user.id
            }
        )

    async def chat_read(self, event):
        await self.send(text_data=json.dumps({
            "type": "read",
            "messageId": event["message_id"],
            "userId": event["user_id"]
        }))

    # ------------------------
    # Database operations
    # ------------------------
    @database_sync_to_async
    def user_in_chat(self):
        # Проверка, что пользователь состоит в чате
        return Chat.objects.filter(
            id=self.chat_id,
            participants__id=self.user.id  # предполагаем, что в Chat есть participants ManyToMany к User
        ).exists()

    @database_sync_to_async
    def create_message(self, text):
        chat = Chat.objects.get(id=self.chat_id)
        return Message.objects.create(
            chat_id=chat.id,
            sender_id=self.user.id,
            text=text
        )

    @database_sync_to_async
    def mark_as_read(self, message_id):
        MessageStatus.objects.update_or_create(
            message_id=message_id,
            user_id=self.user.id,
            defaults={"status": MessageStatus.READ}
        )
