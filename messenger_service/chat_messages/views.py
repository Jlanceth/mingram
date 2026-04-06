from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from chats.models import ChatParticipant
from .models import Message
from .serializers import SendMessageSerializer, MessageSerializer
from .services import send_message


class SendMessageView(APIView):

    def post(self, request):

        serializer = SendMessageSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=400)

        data = serializer.validated_data

        sender_id = 1

        message = send_message(
            sender_id=sender_id,
            receiver_id=data["receiverId"],
            text=data["text"]
        )

        return Response(MessageSerializer(message).data)


class MessageHistoryView(APIView):

    def get(self, request):

        chat_id = request.GET.get("chatId")
        limit = int(request.GET.get("limit", 50))
        offset = int(request.GET.get("offset", 0))
        if not ChatParticipant.objects.filter(
            chat_id=chat_id,
            user_id=1
        ).exists():
            return Response({"error": "No access"}, status=403)
        messages = (
            Message.objects
            .filter(chat_id=chat_id)
            .order_by("-created_at")[offset:offset+limit]
        )

        serializer = MessageSerializer(messages, many=True)

        return Response(serializer.data)
