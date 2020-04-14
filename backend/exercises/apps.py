from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    """Exercises app configuration."""

    name = "exercises"

    def ready(self):
        """Method run when the app is ready.

        Launch the signals handlers.
        """
        # Import signals pre_save

        # Import signals post_save
        from exercises.signals.category import category_saved
        from exercises.signals.difficulty import difficulty_saved
        from exercises.signals.exercise import exercise_saved
        from exercises.signals.section import section_saved
        from exercises.signals.session import session_saved
        from exercises.signals.submission import submission_saved
        from exercises.signals.tag import tag_saved
        from exercises.signals.target_students import target_students_saved

        # Import signals post_delete
        from exercises.signals.category import category_deleted
        from exercises.signals.difficulty import difficulty_deleted
        from exercises.signals.exercise import exercise_deleted_post
        from exercises.signals.section import section_deleted
        from exercises.signals.session import session_deleted
        from exercises.signals.submission import submission_deleted
        from exercises.signals.tag import tag_deleted
        from exercises.signals.target_students import target_students_deleted
