from rest_framework import serializers

from accounts.serializers.user import PublicUserSerializer
from exercises.models.exercise import Exercise
from exercises.serializers.difficulty import DifficultySerializer
from exercises.serializers.section import SectionSerializer
from exercises.serializers.session import SessionSerializer
from exercises.serializers.tag import TagSerializer


class ExerciseSerializer(serializers.ModelSerializer):
    """Serializer for the Exercise model."""

    difficulty = DifficultySerializer()
    tags = TagSerializer(many=True, read_only=True)
    session = SessionSerializer()
    section = SectionSerializer()
    author = PublicUserSerializer()

    class Meta(object):
        """Meta class to select fields."""

        model = Exercise
        fields = "__all__"


class ExerciseCUDSerializer(ExerciseSerializer):
    """Override ExerciseSerializer to create, update and delete operation."""

    class Meta(ExerciseSerializer.Meta):
        """Meta class to select fields."""

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
