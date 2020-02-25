from django.urls import path

from exercises.views.exercice import (
    ExercisesAll,
    ExercisesAllFutureDueDate,
    ExercisesAllBySession,
    ExercisesAllBySessionFutureDueDate,
    ExercisesAllBySection,
    ExercisesAllBySectionFutureDueDate,
    ExercisesAllByCategory,
    ExercisesAllByCategoryFutureDueDate,
    ExerciseGetById,
)

urlpatterns = [
    # /api/exercises/all/
    path("all/", ExercisesAll.as_view(), name="exercises_all"),
    # /api/exercises/all_future/
    path(
        "all_future/", ExercisesAllFutureDueDate.as_view(), name="exercises_all_future"
    ),
    # /api/exercises/by_session/{session_id}
    path(
        "by_session/<int:session_id>",
        ExercisesAllBySession.as_view(),
        name="exercises_by_session",
    ),
    # /api/exercises/by_session_future/{session_id}
    path(
        "by_session_future/<int:session_id>",
        ExercisesAllBySessionFutureDueDate.as_view(),
        name="exercises_by_session_future",
    ),
    # /api/exercises/by_section/{section_id}
    path(
        "by_section/<int:section_id>",
        ExercisesAllBySection.as_view(),
        name="exercises_by_section",
    ),
    # /api/exercises/by_section_future/{section_id}
    path(
        "by_section_future/<int:section_id>",
        ExercisesAllBySectionFutureDueDate.as_view(),
        name="exercises_by_section_future",
    ),
    # /api/exercises/by_category/{category_id}
    path(
        "by_category/<int:category_id>",
        ExercisesAllByCategory.as_view(),
        name="exercises_by_category",
    ),
    # /api/exercises/by_category_future/{category_id}
    path(
        "by_category_future/<int:category_id>",
        ExercisesAllByCategoryFutureDueDate.as_view(),
        name="exercises_by_category_future",
    ),
    # /api/exercises/get/{exercise_id}
    path("get/<int:exercise_id>", ExerciseGetById.as_view(), name="exercise_get"),
]
