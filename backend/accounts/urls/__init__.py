from django.urls import include, path

urlpatterns = [
    # /api/user/*
    path("user/", include("accounts.urls.user")),
    # /api/token/*
    path("token/", include("accounts.urls.token"))
]
