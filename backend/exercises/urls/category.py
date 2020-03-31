from rest_framework import routers

from exercises.views.category import CategoryViewSet

router = routers.DefaultRouter()
router.register("", CategoryViewSet, basename="category")
urlpatterns = router.urls
