from rest_framework import serializers

from exercises.models.section import Section


class SectionSerializer(serializers.ModelSerializer):
    """Serializer for the Section model."""

    class Meta(object):
        """Meta class to select fields."""

        model = Section
        fields = "__all__"


class SectionCUDSerializer(SectionSerializer):
    """Override SectionSerializer to create, update and delete operation."""

    class Meta(SectionSerializer.Meta):
        """Meta class to select fields."""

        fields = (
            "academic_year",
            "name",
            "parent",
            "number",
        )
