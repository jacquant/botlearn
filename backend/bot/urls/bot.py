from rest_framework import routers
from rest_framework import routers
from django.urls import path
from bot.views import AnswerViewSet, TrainingBot

"""
router = routers.DefaultRouter()
router.register("test/", AnswerViewSet, "answer")
urlpatterns = router.urls

"""

urlpatterns = [
    path("test/", AnswerViewSet.as_view(), name="answer"),
    path("train/", TrainingBot.as_view(), name="training")
]
