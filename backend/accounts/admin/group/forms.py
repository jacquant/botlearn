from django import forms
from django.contrib.admin.widgets import FilteredSelectMultiple
from django.contrib.auth.models import Group

from accounts.models.user import User


class GroupAdminForm(forms.ModelForm):
    """Custom form to group for the admin panel."""

    class Meta(object):
        """Meta class override."""

        model = Group
        exclude = []

    # Add the users field.
    users = forms.ModelMultipleChoiceField(
        queryset=User.objects.all(),
        required=False,
        # Use the pretty 'filter_horizontal widget'.
        widget=FilteredSelectMultiple("users", is_stacked=False),
    )

    def __init__(self, *args, **kwargs):
        """Constructor of the GroupAdminForm."""
        # Do the normal form initialisation.
        super().__init__(*args, **kwargs)
        # If it is an existing group (saved objects have a pk).
        if self.instance.pk:
            # Populate the users field with the current Group users.
            self.fields["users"].initial = self.instance.user_set.all()

    def save_m2m(self):
        """Rewrited method to save many to many models."""
        # Add the users to the Group.
        self.instance.user_set.set(self.cleaned_data["users"])

    def save(self, *args, **kwargs):
        """Rewrited method to save model."""
        # Default save
        instance = super().save()
        # Save many-to-many data
        self.save_m2m()
        return instance
