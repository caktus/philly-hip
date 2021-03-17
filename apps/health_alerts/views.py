from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import HealthAlertSubscriberForm


def subscribe(request):

    if request.method == "POST":
        subscribe_form = HealthAlertSubscriberForm(request.POST)

        if subscribe_form.is_valid():
            subscribe_form.save()
            messages.success(
                request,
                (
                    "You are now subscribed to receiving Health Alerts "
                    "from the Philadelphia Department of Public Health."
                ),
            )
            return redirect("/health-alerts/")

    else:
        subscribe_form = HealthAlertSubscriberForm()

    return render(
        request, "health_alerts/health_alert_subscriber.html", {"form": subscribe_form}
    )
