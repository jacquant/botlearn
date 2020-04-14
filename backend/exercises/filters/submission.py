from django_filters import rest_framework as filters

from exercises.models.submission import Submission


class SubmissionFilter(filters.FilterSet):
    """Class to be able to filter Submission on the API view."""

    submission_date = filters.IsoDateTimeFromToRangeFilter(
        field_name="submission_date",
    )
    author_mail = filters.CharFilter(field_name="target__mail")

    class Meta(object):
        """The Meta class that defines the fields available."""

        model = Submission
        fields = ("submission_date", "author_mail", "exercise")
