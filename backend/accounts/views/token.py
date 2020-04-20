from rest_framework_simplejwt.views import TokenObtainPairView

from accounts.serializers.token import UNamurTokenObtainSerializer


class UNamurTokenObtainPairView(TokenObtainPairView):
    """View class that override TokenObtainPairView."""

    serializer_class = UNamurTokenObtainSerializer
