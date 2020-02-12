from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = 'accounts'

    def ready(self):
        from .signals.user.signals import password_reset_token_created