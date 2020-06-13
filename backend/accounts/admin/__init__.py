from django.contrib import admin
from django.contrib.auth.models import (
    Group,
    Permission,
)

from accounts.admin.group.interface import GroupAdmin
from accounts.admin.user.interface import UserAdmin
from accounts.models.user import User

admin.site.unregister(Group)

admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)
admin.site.register(User, UserAdmin)

from django_rest_passwordreset.models import ResetPasswordToken

admin.site.unregister(ResetPasswordToken)
