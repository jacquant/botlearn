from django.urls import path

from exercises.views.session import (
    SessionAll,
    SessionAllFutureDate,
    SessionAllByTarget,
    SessionAllByTargetFutureDate,
    SessionGetById,
)

urlpatterns = [
    # /api/sessions/all/
    path("all/", SessionAll.as_view(), name="sessions_all"),
    # /api/sessions/all_future/
    path("all_future/", SessionAllFutureDate.as_view(), name="sessions_all_future"),
    # /api/sessions/by_target/{target_id}
    path(
        "by_target/<int:target_id>",
        SessionAllByTarget.as_view(),
        name="sessions_by_session",
    ),
    # /api/sessions/by_target_future/{target_id}
    path(
        "by_target_future/<int:target_students_id>",
        SessionAllByTargetFutureDate.as_view(),
        name="sessions_by_target_future",
    ),
    # /api/sessions/get/{session_id}
    path("get/<int:session_id>", SessionGetById.as_view(), name="session_get"),
]
