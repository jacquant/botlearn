from django.apps import AppConfig


class ExercisesConfig(AppConfig):
    name = 'exercises'

    def ready(self):
        from .signals.category import category_update
        from .signals.difficulty import difficulty_update
        from .signals.exercise import exercise_update
        from .signals.section import section_update
        from .signals.session import session_update
        from .signals.tag import tag_update
        from .signals.target_students import target_students_update
