from rest_framework import serializers

from exercises.models.section import Section


class SectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Section
        fields = "__all__"


class SectionCUDSerializer(SectionSerializer):
    class Meta(SectionSerializer.Meta):
        fields = (
            "academic_year",
            "name",
            "parent",
            "number",
        )
