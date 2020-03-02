from django_filters import rest_framework as filters
from exercises.models.submission import Submission


class SubmissionFilter(filters.FilterSet):
    submission_date = filters.IsoDateTimeFromToRangeFilter(field_name="submission_date")
    author_mail = filters.CharFilter(field_name="target__mail")

    class Meta:
        model = Submission
        fields = (
            "submission_date",
            "author_mail",
            "exercise"
        )
