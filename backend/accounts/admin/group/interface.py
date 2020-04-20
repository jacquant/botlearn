from django.contrib import admin

from accounts.admin.group.forms import GroupAdminForm


class GroupAdmin(admin.ModelAdmin):
    """Group class to customize the admin panel."""

    form = GroupAdminForm
    filter_horizontal = ["permissions"]
