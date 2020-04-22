from rest_framework import routers

from exercises.views.error_count import ErrorCountViewSet


router = routers.DefaultRouter()
router.register("", ErrorCountViewSet, basename="error_count")
urlpatterns = router.urls
