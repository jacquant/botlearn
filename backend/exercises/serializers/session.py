from rest_framework import serializers

from accounts.serializers.user import PublicUserSerializer
from exercises.models.session import Session
from exercises.serializers.target_students import TargetStudentsSerializer


class SessionSerializer(serializers.ModelSerializer):
    """Serializer for the Session model."""

    in_charge_persons = PublicUserSerializer(many=True, read_only=True)
    target = TargetStudentsSerializer()

    class Meta(object):
        """Meta class to select fields."""

        model = Session
        fields = "__all__"


class SessionCUDSerializer(SessionSerializer):
    """Override SessionSerializer to create, update and delete operation."""

    class Meta(SessionSerializer.Meta):
        """Meta class to select fields."""

        fields = (
            "name",
            "date",
            "visibility",
            "activated",
            "target",
            "in_charge_persons",
        )
