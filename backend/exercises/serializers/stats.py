from rest_framework import serializers


class StatSerializer(serializers.Serializer):
    number_submissions = serializers.IntegerField()
    errors = serializers.DictField()
