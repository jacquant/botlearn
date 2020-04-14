from rest_framework import serializers

from exercises.models.difficulty import Difficulty


class DifficultySerializer(serializers.ModelSerializer):
    """Serializer for the Difficulty model."""

    class Meta(object):
        """Meta class to define the model and the fields used."""

        model = Difficulty
        fields = "__all__"


class DifficultyCUDSerializer(DifficultySerializer):
    """Override DifficultySerialize to create, update and delete operation."""

    class Meta(DifficultySerializer.Meta):
        """Meta class to select fields."""

        fields = (
            "number",
            "name",
        )
