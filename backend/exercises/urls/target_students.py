from django.urls import path

from exercises.views.target_students import TargetStudentsAll, TargetStudentsGetById


urlpatterns = [
    # /api/target_students/all/
    path("all/", TargetStudentsAll.as_view(), name="target_students_all"),
    # /api/target_students/get/{target_students_id}
    path(
        "get/<int:target_students_id>",
        TargetStudentsGetById.as_view(),
        name="target_students_get",
    ),
]
