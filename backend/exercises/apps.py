from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    name = 'exercises'

    def ready(self):

        # Import signals post_save
        from .signals.category import category_saved
        from .signals.difficulty import difficulty_saved
        from .signals.exercise import exercise_saved
        from .signals.section import section_saved
        from .signals.session import session_saved
        from .signals.tag import tag_saved
        from .signals.target_students import target_students_saved

        # Import signals post_delete
        from .signals.category import category_deleted
        from .signals.difficulty import difficulty_deleted
        from .signals.exercise import exercise_deleted
        from .signals.section import section_deleted
        from .signals.session import session_deleted
        from .signals.tag import tag_deleted
        from .signals.target_students import target_students_deleted

