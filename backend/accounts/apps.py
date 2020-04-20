from django.apps import AppConfig


class AccountsConfig(AppConfig):
    """Account app configuration."""

    name = "accounts"

    def ready(self):
        """Method run when the app is ready.

        Launch the signals handlers.
        """
