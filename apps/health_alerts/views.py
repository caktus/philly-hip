from django.http import HttpResponseRedirect
from django.shortcuts import render

from .forms import HealthAlertsSignUpForm


def sign_up(request):

    if request.method == "POST":
        sign_up_form = HealthAlertsSignUpForm(request.POST)

        if sign_up_form.is_valid():
            sign_up_form.save()
            return HttpResponseRedirect("/health-alerts/", {"subscribed": True})

    else:
        sign_up_form = HealthAlertsSignUpForm()

    return render(
        request, "health_alerts/health_alert_index_page.html", {"form": sign_up_form}
    )
