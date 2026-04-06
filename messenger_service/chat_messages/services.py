from .models import Message, MessageStatus
from chats.models import ChatParticipant
from chats.services import get_or_create_private_chat


def send_message(sender_id, receiver_id, text):

    chat = get_or_create_private_chat(sender_id, receiver_id)

    if not ChatParticipant.objects.filter(
        chat=chat,
        user_id=sender_id
    ).exists():
        raise Exception("User has no access to this chat")

    message = Message.objects.create(
        chat=chat,
        sender_id=sender_id,
        text=text
    )

    # статус для отправителя
    MessageStatus.objects.create(
        message=message,
        user_id=sender_id,
        status=MessageStatus.SENT
    )

    # статус для получателя
    MessageStatus.objects.create(
        message=message,
        user_id=receiver_id,
        status=MessageStatus.DELIVERED
    )

    return message
