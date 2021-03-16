from distutils.util import strtobool

from django.contrib.auth.views import LoginView
from django.shortcuts import render


def handler404(request, *args, **argv):
    response = render(request, "404.html", {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, "500.html", {})
    response.status_code = 500
    return response


class HIPLoginView(LoginView):
    def post(self, request, *args, **kwargs):
        """Set request.session to expire if user should not be remembered."""
        # If the 'remember_me' checkbox value is falsey, then the user's session
        # expires when the broser is closed.
        try:
            remember_user = bool(strtobool(request.POST.get("remember_me", "")))
        except ValueError:
            remember_user = False
        if not remember_user:
            request.session.set_expiry(0)

        return super().post(request, *args, **kwargs)
