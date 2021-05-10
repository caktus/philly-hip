import logging

from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver

from ipware import get_client_ip


logger = logging.getLogger(__name__)


@receiver(user_logged_in)
def log_successful_login(sender, **kwargs):
    """Log when someone logs in to the site."""
    user = kwargs.get("user")
    request = kwargs.get("request")
    ip_address, is_routable = get_client_ip(request)
    logger.info(f"user '{user.email}' has logged in from IP address '{ip_address}'.")


@receiver(user_logged_out)
def log_successful_logout(sender, **kwargs):
    """Log when someone logs out of the site."""
    user = kwargs.get("user")
    # Only log anything if there is a user.
    if user:
        request = kwargs.get("request")
        ip_address, is_routable = get_client_ip(request)
        logger.info(
            f"user '{user.email}' has logged out from IP address '{ip_address}'."
        )
