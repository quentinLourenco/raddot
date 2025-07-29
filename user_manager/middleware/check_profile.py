from django.shortcuts import redirect
from django.urls import resolve


class ProtectRoutesMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        path = request.path_info

        if path.startswith('/auth/'):
            return self.get_response(request)

        # if path.startswith('/static/') or path.startswith('/media/'):
        #     return self.get_response(request)

        if not request.user.is_authenticated:
            return redirect('user_manager:login')

        response = self.get_response(request)
        return response
