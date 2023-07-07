# myapp/middleware.py

from django.shortcuts import redirect

class PreventBackToProfileMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if not request.user.is_authenticated and request.path == 'patient-dashboard':
            return redirect('login')  # Redirect to a custom page

        response = self.get_response(request)
        return response
