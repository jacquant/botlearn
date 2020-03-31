from django.contrib.auth.admin import UserAdmin as BaseAdmin

from .actions import send_reset_password
from .forms import UserCreateForm


class UserAdmin(BaseAdmin):
    add_form = UserCreateForm
    list_display = ("mail", "last_name", "first_name")
    list_filter = ("is_staff", "student")
    actions = [send_reset_password]
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "mail",
                    "last_name",
                    "first_name",
                    "password",
                    "last_login",
                    "student",
                    "student_card",
                    "eid",
                )
            },
        ),
        ("Permissions", {"fields": ("is_staff", "is_superuser", "is_active")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "last_name",
                    "first_name",
                    "mail",
                    "password1",
                    "password2",
                    "student",
                    "student_card",
                    "eid",
                ),
            },
        ),
        ("Permissions", {"classes": ("wide",), "fields": ("is_staff", "is_superuser", "is_active")},),
    )
    search_fields = ("mail", "last_name", "first_name")
    ordering = ("mail", "last_name", "first_name")

    filter_horizontal = ()

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        is_superuser = request.user.is_superuser
        disabled_fields = set()  # type Set[str]

        if not is_superuser:
            disabled_fields |= {"username", "is_superuser", "user_permissions"}

        # Prevent non-superusers from editing their own permissions
        if not is_superuser and obj is not None and obj == request.user:
            disabled_fields |= {
                "is_staff",
                "is_superuser",
                "groups",
                "user_permissions",
            }

        for f in disabled_fields:
            if f in form.base_fields:
                form.base_fields[f].disabled = True

        return form
