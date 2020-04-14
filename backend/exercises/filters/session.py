from django_filters import rest_framework as filters

from exercises.models.session import Session


class SessionFilter(filters.FilterSet):
    """Class to be able to filter Session on the API view."""

    date = filters.IsoDateTimeFromToRangeFilter(field_name="date")
    target_id = filters.NumberFilter(field_name="target__id")
    target_name = filters.CharFilter(field_name="target__name")

    class Meta(object):
        """The Meta class that defines the fields available."""

        model = Session
        fields = (
            "date",
            "target_id",
            "target_name",
        )
