from django_filters import rest_framework as filters

from exercises.models.error import Error
from exercises.models.exercise import Exercise
from exercises.models.submission import Submission


class SubmissionFilter(filters.FilterSet):
    """Class to be able to filter Submission on the API view."""

    submission_date = filters.IsoDateTimeFromToRangeFilter(
        field_name="submission_date",
    )
    author_mail = filters.CharFilter(
        field_name="author__mail", label="Mail de l'auteur"
    )
    exercises = filters.ModelMultipleChoiceFilter(
        field_name="exercise__id",
        to_field_name="id",
        queryset=Exercise.objects.all(),
    )
    specific_errors_by_id = filters.ModelMultipleChoiceFilter(
        field_name="errors__error__id",
        to_field_name="id",
        queryset=Error.objects.all(),
    )
    specific_errors_by_code = filters.ModelMultipleChoiceFilter(
        field_name="errors__error__code",
        to_field_name="code",
        queryset=Error.objects.all(),
    )
    errors_counter_range = filters.RangeFilter(field_name="errors__counter")

    class Meta(object):
        """The Meta class that defines the fields available."""

        model = Submission
        fields = (
            "submission_date",
            "author_mail",
            "exercises",
            "not_executed",
            "final",
            "errors",
            "specific_errors_by_id",
            "specific_errors_by_code",
            "errors_counter_range",
        )
