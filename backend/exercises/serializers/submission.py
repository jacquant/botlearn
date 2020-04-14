from rest_framework import serializers

from accounts.serializers.user import PublicUserSerializer
from exercises.models.exercise import Exercise
from exercises.serializers.exercise import ExerciseSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for the Submission model."""

    author = PublicUserSerializer()
    exercise = ExerciseSerializer()

    class Meta(object):
        """Meta class to select fields."""

        model = Exercise
        fields = "__all__"


class SubmissionCUDSerializer(SubmissionSerializer):
    """Override SubmissionSerializer to create, update and delete operation."""

    class Meta(SubmissionSerializer.Meta):
        """Meta class to select fields."""

        fields = (
            "author",
            "exercise",
            "code_input",
            "code_output",
            "final",
        )
