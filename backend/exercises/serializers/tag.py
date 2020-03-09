from rest_framework import serializers

from exercises.models.tag import Tag


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = "__all__"


class TagCUDSerializer(TagSerializer):
    class Meta(TagSerializer.Meta):
        fields = ("name",)
