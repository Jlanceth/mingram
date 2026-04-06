from django.db import models
from chats.models import Chat


class Message(models.Model):

    chat = models.ForeignKey(
        Chat,
        on_delete=models.CASCADE,
        related_name="messages"
    )

    sender_id = models.IntegerField()
    receiver_id = models.IntegerField()
    text = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    edited_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Message {self.id} from {self.sender_id}"


class MessageStatus(models.Model):

    SENT = "sent"
    DELIVERED = "delivered"
    READ = "read"

    STATUS_CHOICES = [
        (SENT, "Sent"),
        (DELIVERED, "Delivered"),
        (READ, "Read"),
    ]

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="statuses"
    )

    user_id = models.IntegerField()

    status = models.CharField(
        max_length=10,
        choices=STATUS_CHOICES
    )

    timestamp = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("message", "user_id")


class MessageAttachment(models.Model):

    message = models.ForeignKey(
        Message,
        on_delete=models.CASCADE,
        related_name="attachments"
    )

    file = models.FileField(upload_to="attachments/")

    uploaded_at = models.DateTimeField(auto_now_add=True)
