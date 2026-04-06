from django.contrib import admin
from .models import Message, MessageStatus, MessageAttachment

admin.site.register(Message)
admin.site.register(MessageStatus)
admin.site.register(MessageAttachment)
