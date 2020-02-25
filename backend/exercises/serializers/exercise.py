from rest_framework import serializers
from exercises.models.exercise import Exercise


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class ExerciseSaveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = (
            "name",
            "due_date",
            "instruction",
            "difficulty",
            "session",
            "section",
            "tags",
            "project_files",
        )
