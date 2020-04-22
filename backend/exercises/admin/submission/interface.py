from django import forms
from django.contrib import admin
from django.contrib.postgres import fields

from django_ace import AceWidget
from django_json_widget.widgets import JSONEditorWidget


class SubmissionAdminForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(SubmissionAdminForm, self).__init__(*args, **kwargs)
        self.fields["code_input"].widget = AceWidget(
            mode="python", theme="monokai", toolbar=True, width="90%",
        )


class SubmissionAdmin(admin.ModelAdmin):
    """Admin interface for the Submission model."""

    form = SubmissionAdminForm
    formfield_overrides = {
        fields.JSONField: {"widget": JSONEditorWidget(mode="view")},
    }
