from rest_framework import serializers

from exercises.models.target_students import TargetStudents


class TargetStudentsSerializer(serializers.ModelSerializer):
    """Serializer for the TargetStudent model."""

    class Meta(object):
        """Meta class to select fields."""

        model = TargetStudents
        fields = "__all__"


class TargetStudentsCUDSerializer(TargetStudentsSerializer):
    """Override TargetStudent to create, update and delete operation."""

    class Meta(TargetStudentsSerializer.Meta):
        """Meta class to select fields."""

        fields = ("name",)
