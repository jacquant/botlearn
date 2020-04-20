from django_filters import rest_framework as filters

from exercises.models.exercise import Exercise


class ExerciseFilter(filters.FilterSet):
    """Class to be able to filter Exercise on the API view."""

    due_date = filters.IsoDateTimeFromToRangeFilter(field_name="due_date")

    class Meta(object):
        """The Meta class that defines the fields available."""

        model = Exercise
        fields = (
            "due_date",
            "difficulty",
            "session",
            "section",
            "tags",
        )
