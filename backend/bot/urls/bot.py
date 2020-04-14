from rest_framework import routers

from bot.views import (
    AnswerViewSet,
    TrainingBot,
)


router = routers.DefaultRouter()
router.register("test/", AnswerViewSet, basename="answer")
router.register("train/", TrainingBot, basename="training")

urlpatterns = router.urls
