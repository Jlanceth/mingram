from django.db import models


class Chat(models.Model):

    PRIVATE = "private"
    GROUP = "group"

    CHAT_TYPE_CHOICES = [
        (PRIVATE, "Private"),
        (GROUP, "Group"),
    ]

    type = models.CharField(
        max_length=10,
        choices=CHAT_TYPE_CHOICES,
        default=PRIVATE
    )

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Chat {self.id} ({self.type})"


class ChatParticipant(models.Model):

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="participants"
    )

    user_id = models.IntegerField()

    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("chat", "user_id")

    def __str__(self):
        return f"user {self.user_id} in chat {self.chat_id}"
