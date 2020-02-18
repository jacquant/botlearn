from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser

from accounts.models.user import User
from accounts.serializers.user import UserSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class CreateUser(CreateAPIView):
    """
        An Api View which provides a method to save a new user

        # Request: POST

        ## Parameters

        ### Body parameters

        - mail: string of an address email [1..255] char
        - last_name: string [1..40] char
        - first_name: string [1..30] char

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ### User: IsAdminUser

        - The user must be an administrator

        ## Return

        - The return is the created object

        ## Cache:

       - No caching
        """

    permission_classes = (
        IsAuthenticated,
        IsAdminUser,
    )
    model = User
    serializer_class = UserSerializer


class GetUserInfo(RetrieveAPIView):
    """
        An Api View which provides a method to get the user information

        # Request: GET

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a UserSerializer object corresponding of the user token

        ## Cache:

       - No caching
        """

    permission_classes = (IsAuthenticated,)
    serializer_class = UserSerializer

    def get_queryset(self):
        key = "users_all"
        if key in cache:
            return cache.get(key)
        else:
            users = User.objects.all()
            cache.set(key, users, timeout=CACHE_TTL)
            return users

    def get_object(self):
        return self.request.user
