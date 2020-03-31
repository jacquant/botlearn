from rest_framework import serializers

from exercises.models.exercise import Exercise
from exercises.serializers.tag import TagSerializer
from exercises.serializers.difficulty import DifficultySerializer
from exercises.serializers.section import SectionSerializer
from exercises.serializers.session import SessionSerializer
from accounts.serializers.user import PublicUserSerializer


class ExerciseSerializer(serializers.ModelSerializer):
    difficulty = DifficultySerializer()
    tags = TagSerializer(many=True, read_only=True)
    session = SessionSerializer()
    section = SectionSerializer()
    author = PublicUserSerializer()

    class Meta:
        model = Exercise
        fields = "__all__"


class ExerciseCUDSerializer(ExerciseSerializer):
    class Meta(ExerciseSerializer.Meta):
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
