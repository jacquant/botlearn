from django.urls import path

from exercises.views.stats import (
    ErrorsByAuthor,
    ErrorsByExercise,
    ErrorsByExerciseFinal,
    ErrorsBySection,
    ErrorsBySession,
)

urlpatterns = [
    path(
        "errors_by_section/<int:section_id>/",
        ErrorsBySection.as_view(),
        name="errors_by_section",
    ),
    path(
        "errors_by_session/<int:session_id>/",
        ErrorsBySession.as_view(),
        name="errors_by_session",
    ),
    path(
        "errors_by_exercise/<int:exercise_id>/",
        ErrorsByExercise.as_view(),
        name="errors_by_exercise",
    ),
    path(
        "errors_by_exercise_final/<int:exercise_id>/",
        ErrorsByExerciseFinal.as_view(),
        name="errors_by_exercise_final",
    ),
    path(
        "errors_by_author/<str:author_mail>/",
        ErrorsByAuthor.as_view(),
        name="errors_by_author",
    ),
]
