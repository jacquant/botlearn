from django.urls import path

from exercises.views.difficulty import DifficultyAll, DifficultyGetById


urlpatterns = [
    # /api/difficulties/all/
    path("all/", DifficultyAll.as_view(), name="difficulties_all"),
    # /api/difficulties/get/{difficulty_id}
    path("get/<int:difficulty_id>", DifficultyGetById.as_view(), name="difficulty_get"),
]
