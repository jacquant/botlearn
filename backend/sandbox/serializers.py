from abc import ABCMeta

from rest_framework import serializers


class CodeSerializer(serializers.Serializer):
    def create(self, validated_data):
        pass

    def update(self, instance, validated_data):
        pass

    code_input = serializers.CharField()


class CodeSerializerLint(CodeSerializer):
    filename = serializers.CharField()
    translate = serializers.BooleanField()


class CodeSerializerExercise(CodeSerializer):
    exercise_id = serializers.IntegerField()
    exercise_filename = serializers.CharField()
