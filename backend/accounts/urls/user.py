from django.urls import path

from accounts.views.user import (
    CreateUser,
    GetUserInfo,
    UpdateUser)

urlpatterns = [
    # /api/user/create/
    path("create/", CreateUser.as_view(), name="create_user"),
    # /api/user/get/
    path("get/", GetUserInfo.as_view(), name="get_user"),
    # /api/user/update/
    path("update", UpdateUser.as_view(), name="update_user")
]
