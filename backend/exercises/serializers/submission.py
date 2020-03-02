from rest_framework import serializers

from exercises.models.exercise import Exercise
from exercises.serializers.exercise import ExerciseSerializer
from accounts.serializers.user import PublicUserSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    author = PublicUserSerializer()
    exercise = ExerciseSerializer()

    class Meta:
        model = Exercise
        fields = "__all__"


class SubmissionCUDSerializer(SubmissionSerializer):
    class Meta(SubmissionSerializer.Meta):
        fields = (
            "author",
            "exercise",
            "code_input",
            "code_output",
            "final",
        )
