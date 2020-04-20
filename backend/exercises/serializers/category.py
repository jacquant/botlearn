from rest_framework import serializers

from exercises.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    """Serializer for the Category model."""

    class Meta(object):
        """Meta class to define the model and the fields used."""

        model = Category
        fields = "__all__"


class CategoryCUDSerializer(CategorySerializer):
    """Override CategorySerializer to create, update and delete operation."""

    class Meta(CategorySerializer.Meta):
        """Meta class to select fields."""

        fields = ("name",)
