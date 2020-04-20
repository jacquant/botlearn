from rest_framework import serializers

from exercises.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    """Serializer for the Tag model."""

    class Meta(object):
        """Meta class to select fields."""

        model = Tag
        fields = "__all__"


class TagCUDSerializer(TagSerializer):
    """Override TagSerializer to create, update and delete operation."""

    class Meta(TagSerializer.Meta):
        """Meta class to select fields."""

        fields = ("name",)
