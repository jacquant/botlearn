from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission

from .user.interface import UserAdmin
from accounts.models.user import User
from .group.interface import GroupAdmin

admin.site.unregister(Group)

admin.site.register(Group, GroupAdmin)
admin.site.register(Permission)
admin.site.register(User, UserAdmin)
