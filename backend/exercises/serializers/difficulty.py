from rest_framework import serializers

from exercises.models.difficulty import Difficulty


class DifficultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Difficulty
        fields = "__all__"
