from rest_framework import routers

from exercises.views.submission import SubmissionViewSet

router = routers.DefaultRouter()
router.register("", SubmissionViewSet, basename="submission")
urlpatterns = router.urls
