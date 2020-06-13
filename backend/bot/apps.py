from django.apps import AppConfig


class BotConfig(AppConfig):
    """Bot app configuration."""

    name = "bot"

    def ready(self):
        """Method run when the app is ready.

        Launch the signals handlers.
        """
        # Import signals pre_save

        # Import signals post_save
        from bot.signals.answer import answer_saved
        from bot.signals.question import question_saved

        # Import signals post_delete
        from bot.signals.answer import answer_deleted
        from bot.signals.question import question_deleted

