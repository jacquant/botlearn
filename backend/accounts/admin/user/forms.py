from django.contrib.auth.forms import UserCreationForm

from accounts.models.user import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ["mail", "last_name", "first_name"]
