from django.contrib.auth.forms import UserCreationForm

from accounts.models.user import User


class UserCreateForm(UserCreationForm):
    """Custom form to create user in admin panel."""

    class Meta(object):
        """The Meta Class of the UserCreateForm."""

        model = User
        fields = ["mail", "last_name", "first_name"]
