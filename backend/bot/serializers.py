from rest_framework import serializers


class QuestionSerializer(serializers.Serializer):
    text = serializers.CharField()
