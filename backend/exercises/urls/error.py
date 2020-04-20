from rest_framework import routers

from exercises.views.error import ErrorViewSet


router = routers.DefaultRouter()
router.register("", ErrorViewSet, basename="error")
urlpatterns = router.urls
