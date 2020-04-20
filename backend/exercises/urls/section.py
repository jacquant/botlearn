from rest_framework import routers

from exercises.views.section import SectionViewSet


router = routers.DefaultRouter()
router.register("", SectionViewSet, basename="section")
urlpatterns = router.urls
