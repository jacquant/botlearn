from rest_framework import serializers

from exercises.models.error import Error


class ErrorSerializer(serializers.ModelSerializer):
    """Serializer for the Error model."""

    class Meta(object):
        """Meta class to define the model and the fields used."""

        model = Error
        fields = "__all__"


class ErrorCUDSerializer(ErrorSerializer):
    """Override ErrorSerializer to create, update and delete operation."""

    class Meta(ErrorSerializer.Meta):
        """Meta class to select fields."""

        fields = (
            "code",
            "message",
            "type_error",
        )
