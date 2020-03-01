from django_filters import rest_framework as filters
from exercises.models.exercise import Exercise


class ExerciseFilter(filters.FilterSet):
    due_date = filters.IsoDateTimeFromToRangeFilter(field_name="due_date")

    class Meta:
        model = Exercise
        fields = (
            "due_date",
            "difficulty",
            "session",
            "section",
            "tags",
        )
