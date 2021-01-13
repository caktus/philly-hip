import os

from .base import *  # noqa


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "m-u!e0jum^(+nt1+6@31+jl_zwc6yltugtv7%!2k(6l!c@=0n@"

# SECURITY WARNING: define the correct hosts in production!
ALLOWED_HOSTS = ["*"]
INTERNAL_IPS = ("127.0.0.1",)

if os.getenv("DEBUG_TOOLBAR", "True") == "True":
    INSTALLED_APPS += [
        "debug_toolbar",
    ]
    MIDDLEWARE += ["debug_toolbar.middleware.DebugToolbarMiddleware"]

EMAIL_BACKEND = "django.core.mail.backends.console.EmailBackend"
