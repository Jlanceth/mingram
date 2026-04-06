from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .services import UserServiceClient


class UserSearchView(APIView):

    def get(self, request):
        query = request.GET.get("q", "")

        if not query:
            return Response([], status=200)

        users = UserServiceClient.search_users(query)

        if users is None:
            return Response(
                {"error": "User service unavailable"},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        return Response(users)
