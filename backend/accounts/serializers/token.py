import requests
from rest_framework import (
    exceptions,
    serializers,
)
from rest_framework_simplejwt.state import User
from rest_framework_simplejwt.tokens import RefreshToken


class UNamurTokenObtainSerializer(serializers.Serializer):
    """Serializer used to authenticate an user by UNamur Oauth."""

    eid = serializers.CharField(max_length=10)
    password = serializers.CharField(max_length=100)

    @classmethod
    def get_token(cls, user):
        """Method to get the token for the requested user.

        :param user: the user mail that request a new token
        :type user: str
        :return: The token refreshed for the specific user
        :rtype: str
        """
        return RefreshToken.for_user(user)

    def validate(self, attrs):
        """Validate the user that request a token.

        :param attrs: The attributes given by the view.
        :type attrs: dict
        :raises exceptions.AuthenticationFailed: The authentication was
                                                 unsuccessful
        :return: A dictionnary with both tokens, the refresh and the access.
        :rtype: dict
        """
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
                generated_tokens = {}
                refresh = self.get_token(user[0])

                generated_tokens["refresh"] = str(refresh)
                generated_tokens["access"] = str(refresh.access_token)
                return generated_tokens
            raise exceptions.AuthenticationFailed(
                req.status_code, "authentication_error"
            )
        raise exceptions.AuthenticationFailed(
            self.error_messages["no_active_account"], "no_active_account"
        )
