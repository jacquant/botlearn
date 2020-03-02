from rest_framework import routers

from exercises.views.tag import TagViewSet

router = routers.DefaultRouter()
router.register("", TagViewSet, basename="tag")
urlpatterns = router.urls
