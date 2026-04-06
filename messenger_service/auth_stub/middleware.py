class DevAuthMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer"):
            token = auth_header.split(" ")[1]
            request.user_id = int(token)
        else:
            request.user_id = None

        response = self.get_response(request)
        return response
