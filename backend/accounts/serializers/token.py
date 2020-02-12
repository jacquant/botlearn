import requests
from rest_framework import exceptions, serializers
from rest_framework_simplejwt.state import User
from rest_framework_simplejwt.tokens import RefreshToken


class UNamurTokenObtainSerializer(serializers.Serializer):
    eid = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=100)

    @classmethod
    def get_token(cls, user):
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        user = User.objects.filter(eid=attrs["eid"], is_active=True)
        if user.exists():
            payload = {
                "user": attrs["eid"],
                "password": attrs["password"],
            }
            req = requests.post(
                "https://auth.unamur.be", payload, allow_redirects=False
            )
            if req.status_code == 303:
                data = {}
                refresh = self.get_token(user[0])

                data["refresh"] = str(refresh)
                data["access"] = str(refresh.access_token)
                return data
            else:
                raise exceptions.AuthenticationFailed()
        else:
            raise exceptions.AuthenticationFailed(
                self.error_messages["no_active_account"], "no_active_account",
            )
