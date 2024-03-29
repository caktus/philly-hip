from django.contrib import messages
from django.shortcuts import redirect, render

from .forms import (
    CodeRedCodeBlueSubscriberForm,
    CommunityResponseSubscriberForm,
    DrugOverdoseSubscriberForm,
    InternalAlertsSubscriberForm,
    PublicHealthPreparednessSubscriberForm,
)


from apps.common.utils import (  # isort: skip
    get_emergency_communications_page_url,
    get_next_url_from_request,
)


def generic_notification_signup(
    request,
    form,
    success_message,
    success_url,
    close_url,
    template_name="notifications/notification_signup.html",
    context={},
):
    """A generic view to handle subscribing through a form."""
    if request.method == "POST":
        subscribe_form = form(request.POST)
        if subscribe_form.is_valid():
            subscribe_form.save()
            messages.success(request, success_message)
            return redirect(success_url)
    else:
        subscribe_form = form()

    context["close_url"] = close_url
    context["next"] = success_url
    context["form"] = subscribe_form
    return render(request, template_name, context)


def internal_alerts_signup(request):
    """View for managing sign ups for internal alerts."""
    success_message = (
        "You are now subscribed to alerts from the Philadelphia Department of "
        "Public Health Internal Employee Alert System"
    )
    next_url = get_next_url_from_request(request)
    if next_url:
        success_url = close_url = next_url
    else:
        success_url = close_url = get_emergency_communications_page_url()

    return generic_notification_signup(
        request,
        InternalAlertsSubscriberForm,
        success_message,
        success_url,
        close_url,
        "notifications/notification_signup.html",
        {"title": "Internal Employee Alert System"},
    )


def community_notifications_signup(request):
    """View for managing sign ups for community response notifications."""
    success_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health for sharing with communities within Philadelphia."
    )
    next_url = get_next_url_from_request(request)
    if next_url:
        success_url = close_url = next_url
    else:
        success_url = close_url = get_emergency_communications_page_url()

    return generic_notification_signup(
        request,
        CommunityResponseSubscriberForm,
        success_message,
        success_url,
        close_url,
        "notifications/notification_signup.html",
        {"title": "Community Response Partner Network"},
    )


def drug_notifications_signup(request):
    """View for managing sign ups for drug overdose notifications."""
    success_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to drug overdoses."
    )
    next_url = get_next_url_from_request(request)
    if next_url:
        success_url = close_url = next_url
    else:
        success_url = close_url = get_emergency_communications_page_url()

    return generic_notification_signup(
        request,
        DrugOverdoseSubscriberForm,
        success_message,
        success_url,
        close_url,
        "notifications/notification_signup.html",
        {"title": "Drug Overdose Notification Network"},
    )


def codeblue_codered_notifications_signup(request):
    """View for managing sign ups for Code Red/Code Blue notifications."""
    success_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to Code Red/Code Blue events."
    )
    next_url = get_next_url_from_request(request)
    if next_url:
        success_url = close_url = next_url
    else:
        success_url = close_url = get_emergency_communications_page_url()

    return generic_notification_signup(
        request,
        CodeRedCodeBlueSubscriberForm,
        success_message,
        success_url,
        close_url,
        "notifications/notification_signup.html",
        {"title": "Code Red and Blue Notifications"},
    )


def public_health_preparedness_signup(request):
    """View for managing sign ups for public health preparedness notifications."""
    success_message = (
        "You are now subscribed to notifications from the Philadelphia Department "
        "of Public Health related to public health preparedness."
    )
    next_url = get_next_url_from_request(request)
    if next_url:
        success_url = close_url = next_url
    else:
        success_url = close_url = get_emergency_communications_page_url()

    return generic_notification_signup(
        request,
        PublicHealthPreparednessSubscriberForm,
        success_message,
        success_url,
        close_url,
        "notifications/notification_signup.html",
        {"title": "Public Health Preparedness Notifications"},
    )
