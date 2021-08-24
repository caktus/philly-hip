from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = "apps.users"

    def ready(self):
        # Import the signals here, so that they are registered.
        from apps.users import signals  # noqa
