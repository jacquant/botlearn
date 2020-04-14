from rest_framework import routers

from exercises.views.target_students import TargetStudentsViewSet


router = routers.DefaultRouter()
router.register("", TargetStudentsViewSet, basename="target_students")
urlpatterns = router.urls
