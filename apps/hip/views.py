from distutils.util import strtobool

from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.core.files.uploadhandler import TemporaryFileUploadHandler
from django.shortcuts import redirect, render, reverse
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt, csrf_protect

from wagtail.documents.views.multiple import AddView

from apps.common.utils import (
    get_bigcities_home_page_url,
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
    # Users in the "Big Cities" Group get redirected to the BigCitiesHomePage.
    if request.user.groups.filter(name="Closed POD").exists():
        return redirect(get_closedpod_home_page_url())
    elif request.user.groups.filter(name="PCW MSA").exists():
        return redirect(get_pcwmsa_home_page_url())
    elif request.user.groups.filter(name="Big Cities").exists():
        return redirect(get_bigcities_home_page_url())
    # All other authenticated users are redirected to the home page.
    return redirect(get_home_page_url())


class HIPDocumentAddView(AddView):
    """
    Custom view for adding HIPDocuments.

    This class exists for the purpose of forcing the request's upload handler
    to be TemporaryFileUploadHandler, which requires overriding the dispatch() method,
    based on the Django documentation for setting upload handlers for a request:
    https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/#modifying-upload-handlers-on-the-fly
    """

    @method_decorator(csrf_exempt)
    def dispatch(self, request):
        """
        Use the TemporaryFileUploadHandler before any other handlers.

        Note: we use the TemporaryFileUploadHandler so that our
        scan_pdf_for_malicious_content() function can use pdfid, which expects
        a path to the PDF file.

        Other note: changing the request's upload_handlers means that this function
        must be CSRF-exempt. To keep CSRF protection, we return self._dispatch(),
        which is CSRF-protected. This code was written based on the Django
        documentation for changing upload handlers for a request:
        https://docs.djangoproject.com/en/3.2/topics/http/file-uploads/#modifying-upload-handlers-on-the-fly
        """
        request.upload_handlers.insert(0, TemporaryFileUploadHandler(request))
        return self._dispatch(request)

    @method_decorator(csrf_protect)
    def _dispatch(self, request):
        """A private CSRF-protected view, returned from self.dispatch()."""
        return super().dispatch(request)
