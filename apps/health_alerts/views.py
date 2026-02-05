from apps.notifications.views import generic_notification_signup

from .forms import HealthAlertSubscriberForm


# On 02/04/26 Brandon Horvath emailed us asking if we could link
# to a new form and stop using this one. He said that this form
# can be deleted in the future.
def subscribe(request):
    """View for managing sign ups for health alerts."""
    success_message = (
        "You are now subscribed to receiving Health Alerts from the Philadelphia "
        "Department of Public Health."
    )
    success_url = close_url = "/health-alerts/"
    return generic_notification_signup(
        request,
        HealthAlertSubscriberForm,
        success_message,
        success_url,
        close_url,
        "notifications/notification_signup.html",
        {"title": "Health Alerts Sign Up Form"},
    )
