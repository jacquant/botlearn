from django.urls import path

from .views import CodeExecute, CodeLint, CodeFormat

urlpatterns = [
    path("execute/", CodeExecute.as_view(), name="execute"),
    path("lint/", CodeLint.as_view(), name="lint"),
    path("format/", CodeFormat.as_view(), name="format"),
]
