from django.apps import AppConfig


class AccountsConfig(AppConfig):
    name = "accounts"

    def ready(self):
        from .signals.user import password_reset_token_created
        from .signals.user import user_update
