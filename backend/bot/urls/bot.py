from django.urls import path

from bot.views import (
    AnswerViewSet,
    TrainingBot,
)


urlpatterns = [
    path("test/", AnswerViewSet.as_view(), name="answer"),
    path("train/", TrainingBot.as_view(), name="training")
]
