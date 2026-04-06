from django.urls import path
from .views import SendMessageView, MessageHistoryView

urlpatterns = [
    path("messages/", SendMessageView.as_view()),
    path("messages/history/", MessageHistoryView.as_view()),
]
