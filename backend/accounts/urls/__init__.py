from django.urls import include, path

urlpatterns = [
    # /api/token/*
    path("token/", include("accounts.urls.token.urls"))
]
