from distutils.util import strtobool

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render, reverse

from apps.common.utils import (
    get_closedpod_home_page_url,
    get_home_page_url,
    get_pcwmsa_home_page_url,
)


def handler404(request, *args, **argv):
    response = render(request, "404.html", {})
    response.status_code = 404
    return response


def handler500(request, *args, **argv):
    response = render(request, "500.html", {})
    response.status_code = 500
    return response


class HIPLoginView(LoginView):
    def get(self, request, *args, **kwargs):
        """GETting the HIPLoginView redirects authenticated users to the auth_view_router."""
        if request.user.is_authenticated:
            return redirect(reverse("auth_view_router"))
        return super().get(request, *args, **kwargs)

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


@login_required
def authenticated_view_router(request, *args, **kwargs):
    """Determine which home page an authenticated user should go to, and redirect them there."""
    # Users in the "Closed POD" Group get redirected to the ClosedPODHomePage.
    # Users in the "PCW MSA" Group get redirected to the PCWMSAHomePage.
    if request.user.groups.filter(name="Closed POD").exists():
        return redirect(get_closedpod_home_page_url())
    elif request.user.groups.filter(name="PCW MSA").exists():
        return redirect(get_pcwmsa_home_page_url())
    # All other authenticated users are redirected to the home page.
    return redirect(get_home_page_url())
