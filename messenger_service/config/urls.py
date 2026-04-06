
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/", include("chat_messages.urls")),
    path("api/users/", include("auth_stub.urls")),
    path("api/chats/", include("chats.urls")),
]
