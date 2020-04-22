from rest_framework import serializers


class CodeSerializer(serializers.Serializer):
    """Base class Serializer for code."""

    code_input = serializers.CharField()


class CodeSerializerLint(CodeSerializer):
    """Serializer class used to lint code."""

    filename = serializers.CharField()
    translate = serializers.BooleanField()


class CodeSerializerExercise(CodeSerializer):
    """Serializer class used to execute code."""

    final = serializers.BooleanField()
    exercise_id = serializers.IntegerField()
    filename = serializers.CharField()
