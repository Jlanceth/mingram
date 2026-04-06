from django.contrib import admin
from .models import Chat, ChatParticipant

class ChatParticipantInline(admin.TabularInline):
    model = ChatParticipant
    extra = 1  # сколько пустых полей сразу показывать
    min_num = 1
    can_delete = True

class ChatAdmin(admin.ModelAdmin):
    inlines = [ChatParticipantInline]


admin.site.register(Chat, ChatAdmin)
admin.site.register(ChatParticipant)
