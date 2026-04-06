from .models import Chat, ChatParticipant


def get_or_create_private_chat(user1_id, user2_id):
    chats = Chat.objects.filter(type=Chat.PRIVATE)

    for chat in chats:
        participants = set(
            chat.participants.values_list("user_id", flat=True)
        )
        if participants == {user1_id, user2_id}:
            return chat
    
    chat = Chat.objects.create(type=Chat.PRIVATE)

    ChatParticipant.objects.create(chat=chat, user_id=user1_id)
    ChatParticipant.objects.create(chat=chat, user_id=user2_id)

    return chat
