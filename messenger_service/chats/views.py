from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Chat


class ChatListView(APIView):

    def get(self, request):
        user_id = 1  # потом заменишь на auth

        chats = Chat.objects.filter(
            participants__user_id=user_id
        ).distinct()

        result = []

        for chat in chats:
            participants = list(
                chat.participants.values_list("user_id", flat=True)
            )

            last_message = chat.messages.order_by("-created_at").first()

            result.append({
                "id": chat.id,
                "type": chat.type,
                "participants": participants,
                "lastMessage": last_message.text if last_message else None
            })

        return Response(result)
