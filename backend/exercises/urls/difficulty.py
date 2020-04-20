from rest_framework import routers

from exercises.views.difficulty import DifficultyViewSet


router = routers.DefaultRouter()
router.register("", DifficultyViewSet, basename="difficulty")
urlpatterns = router.urls
