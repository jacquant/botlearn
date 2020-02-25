from django.contrib import admin

from .forms import GroupAdminForm


class GroupAdmin(admin.ModelAdmin):
    form = GroupAdminForm
    filter_horizontal = ["permissions"]
