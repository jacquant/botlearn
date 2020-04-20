from rest_framework import routers

from exercises.views.session import SessionViewSet


router = routers.DefaultRouter()
router.register("", SessionViewSet, basename="session")
urlpatterns = router.urls
