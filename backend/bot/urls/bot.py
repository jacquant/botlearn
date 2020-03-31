from django.urls import path
from bot.views import AnswerViewSet


urlpatterns = [
    path("test/", AnswerViewSet.as_view(), name="answer"),
]
