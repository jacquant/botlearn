from rest_framework import serializers

from accounts.serializers.user import PublicUserSerializer
from exercises.models.session import Session
from exercises.serializers.target_students import TargetStudentsSerializer


class SessionSerializer(serializers.ModelSerializer):
    in_charge_persons = PublicUserSerializer(many=True, read_only=True)
    target = TargetStudentsSerializer()

    class Meta:
        model = Session
        fields = "__all__"


class SessionCUDSerializer(SessionSerializer):
    class Meta(SessionSerializer.Meta):
        fields = (
            "name",
            "date",
            "visibility",
            "activated",
            "target",
            "in_charge_persons",
        )
