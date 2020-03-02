from rest_framework import serializers

from exercises.models.category import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = "__all__"


class CategoryCUDSerializer(CategorySerializer):
    class Meta(CategorySerializer.Meta):
        fields = ("name",)
