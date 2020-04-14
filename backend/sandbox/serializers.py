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

    exercise_id = serializers.IntegerField()
    exercise_filename = serializers.CharField()
