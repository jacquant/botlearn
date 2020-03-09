from rest_framework import routers

from exercises.views.exercise import ExerciseViewSet

router = routers.DefaultRouter()
router.register("", ExerciseViewSet, basename="exercise")
urlpatterns = router.urls
