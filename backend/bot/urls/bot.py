from rest_framework import routers
from rest_framework import routers
from django.urls import path
from bot.views import AnswerViewSet

"""
router = routers.DefaultRouter()
router.register("test/", AnswerViewSet, "answer")
urlpatterns = router.urls

"""

urlpatterns = [
    path("test/", AnswerViewSet.as_view(), name="answer"),
]

