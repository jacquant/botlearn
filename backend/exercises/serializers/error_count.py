from rest_framework import serializers

from exercises.models.error_count import ErrorCount
from exercises.serializers.error import ErrorSerializer


class ErrorCountSerializer(serializers.ModelSerializer):
    """Serializer for the ErrorCount model."""

    error = ErrorSerializer()

    class Meta(object):
        """Meta class to define the model and the fields used."""

        model = ErrorCount
        fields = "__all__"


class ErrorCountCUDSerializer(ErrorCountSerializer):
    """Override ErrorCountSerializer to create, update and delete operation."""

    class Meta(ErrorCountSerializer.Meta):
        """Meta class to select fields."""

        fields = (
            "error",
            "counter",
        )
