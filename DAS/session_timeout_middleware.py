from django.contrib.auth import logout

class SessionIdleTimeoutMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if the user is authenticated
        if request.user.is_authenticated:
            # Check if the session has expired
            if request.session.get_expiry_age() <= 0:
                # Log out the user
                logout(request)

        response = self.get_response(request)
        return response
