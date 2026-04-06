from rest_framework import serializers
from .models import Message


class SendMessageSerializer(serializers.Serializer):
    receiverId = serializers.IntegerField()
    text = serializers.CharField()


class MessageSerializer(serializers.ModelSerializer):

    senderId = serializers.IntegerField(source="sender_id")
    chatId = serializers.IntegerField(source="chat_id")
    receiverId = serializers.IntegerField(source="receiver_id")

    class Meta:
        model = Message
        fields = [
            "id",
            "chatId",
            "senderId",
            "receiverId",
            "text",
            "created_at",
        ]
