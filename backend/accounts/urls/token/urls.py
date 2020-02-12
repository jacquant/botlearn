from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from accounts.views.token import UNamurTokenObtainPairView

urlpatterns = [
    # /api/token/login/
    path("login/", TokenObtainPairView.as_view(), name="login"),
    # /api/token/refresh/
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    # /api/token/verify/
    path("verify/", TokenVerifyView.as_view(), name="verify"),
    # /api/token/login_by_unamur/
    path("login_by_unamur/", UNamurTokenObtainPairView.as_view(), name="login_unamur")
]
