from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import HealthAlertSubscriberForm


def sign_up(request):

    if request.method == "POST":
        sign_up_form = HealthAlertSubscriberForm(request.POST)

        if sign_up_form.is_valid():
            sign_up_form.save()
            messages.success(
                request,
                (
                    "You are now subscribed to receiving Health Alerts "
                    "from the Philadelphia Department of Public Health."
                ),
            )
            return redirect("/health-alerts/")

    else:
        sign_up_form = HealthAlertSubscriberForm()

    return render(
        request, "health_alerts/health_alert_subscriber.html", {"form": sign_up_form}
    )
