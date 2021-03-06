from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.http import HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

from apps.common.utils import closedpod_user_check

from .forms import ClosedPODContactInformationForm
from .models import ClosedPODContactInformation, ClosedPODHomePage


@require_http_methods(["GET"])
@user_passes_test(closedpod_user_check)
def closedpod_contact_information(request):
    """Return the request.user's ClosedPODContactInformation."""
    home_page = ClosedPODHomePage.objects.live().first()
    if not home_page:
        return HttpResponseBadRequest(
            content=(
                "Closed-Pod home page must be created and "
                "made live before accessing this page."
            )
        )

    if hasattr(request.user, "closedpodcontactinformation"):
        contact_info = request.user.closedpodcontactinformation
    else:
        contact_info = ClosedPODContactInformation(user=request.user)
    return render(
        request,
        "auth_content/closedpod_contact_information.html",
        {
            "contact_info": contact_info,
            "show_closedpod_sidebar": True,
            "closedpod_home_url": home_page.url,
            "closedpod_children_pages": home_page.get_children(),
        },
    )


@require_http_methods(["GET", "POST"])
@user_passes_test(closedpod_user_check)
def closedpod_contact_information_edit(request):
    """Update the request.user's ClosedPODContactInformation."""
    if request.method == "GET":
        # If the request.user has a ClosedPODContactInformation, then instantiate
        # the form with it; otherwise, the form has empty data.
        if hasattr(request.user, "closedpodcontactinformation"):
            form = ClosedPODContactInformationForm(
                instance=request.user.closedpodcontactinformation
            )
        else:
            form = ClosedPODContactInformationForm()
        # Render the page with the form.
        return render(
            request,
            "auth_content/closedpod_contact_information_edit.html",
            {"form": form},
        )
    else:
        # If the request.user has a ClosedPODContactInformation, then instantiate
        # the form with it and the request.POST data; otherwise, instantiate the
        # form with the request.POST data.
        form_data = request.POST.copy()
        form_data["user"] = request.user
        if hasattr(request.user, "closedpodcontactinformation"):
            form = ClosedPODContactInformationForm(
                form_data, instance=request.user.closedpodcontactinformation
            )
        else:
            form = ClosedPODContactInformationForm(form_data)
        # If the form is valid, then save it, and redirect the user to the
        # "closedpod_contact_information" view.
        if form.is_valid():
            instance = form.save(commit=False)
            # 'user' field is not editable in the form since user is only able to edit
            # their own info. Set user appropriately here.
            instance.user = request.user
            instance.save()
            messages.success(request, "Contact information has been updated")
            return redirect("closedpod_contact_information")
        else:
            # The form is not valid, so render the page (with the form errors).
            return render(
                request,
                "auth_content/closedpod_contact_information_edit.html",
                {"form": form},
            )
