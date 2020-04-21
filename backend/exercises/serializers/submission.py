from rest_framework import serializers

from accounts.serializers.user import PublicUserSerializer
from exercises.models.submission import Submission
from exercises.serializers.error_count import ErrorCountCUDSerializer
from exercises.serializers.exercise import ExerciseSerializer


class SubmissionSerializer(serializers.ModelSerializer):
    """Serializer for the Submission model."""

    author = PublicUserSerializer()
    errors = ErrorCountCUDSerializer(many=True, read_only=True)

    class Meta(object):
        """Meta class to select fields."""

        model = Submission
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
            "errors",
        )
