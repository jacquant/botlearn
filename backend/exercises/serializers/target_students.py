from rest_framework import serializers

from exercises.models.target_students import TargetStudents


class TargetStudentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TargetStudents
        fields = "__all__"
