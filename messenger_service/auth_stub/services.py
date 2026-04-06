import requests
from django.conf import settings


class UserServiceClient:

    @classmethod
    def search_users(cls, query):
        try:
            response = requests.get(
                f"{settings.USER_SERVICE_URL}/users/search/",
                params={"q": query},
                timeout=3
            )

            response.raise_for_status()

            data = response.json()

            # нормализация ответа
            return [
                {
                    "id": user.get("id"),
                    "username": user.get("username"),
                }
                for user in data
            ]

        except requests.RequestException:
            return [
                {"id": 1, "username": "test_user_1"},
                {"id": 2, "username": "test_user_2"},
            ]
