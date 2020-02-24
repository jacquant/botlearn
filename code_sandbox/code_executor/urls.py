from django.urls import path

from .views import CodeView

urlpatterns = [
    path("execute/", CodeView.as_view(), name="execute-python-code")
]
