from rest_framework import serializers

from exercises.models.session import Session


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = "__all__"
