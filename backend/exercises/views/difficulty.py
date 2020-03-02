from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, viewsets

from exercises.models.difficulty import Difficulty
from exercises.serializers.difficulty import DifficultySerializer, DifficultyCUDSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class DifficultyViewSet(viewsets.ModelViewSet):
    lookup_url_kwarg = "difficulty_id"
    lookup_field = "id"

    def get_queryset(self):
        key = "difficulties_all"
        if key in cache:
            return cache.get(key)
        else:
            difficulties = Difficulty.objects.all()
            cache.set(key, difficulties, timeout=CACHE_TTL)
            return difficulties

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return DifficultySerializer
        else:
            return DifficultyCUDSerializer

    def list(self, request, *args, **kwargs):
        """
        An Api View which provides a method to request a list of Difficulty objects

        # Request: GET

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

         ## Return

        - The return is a **List** of DifficultySerializer objects

        ## Cache:

        - The list is saved in the redis cache if the key do not exist
        - Else return the list already saved in the cache
        - The cache is delete when a difficulty object is saved or deleted
        """
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        An Api View which provides a method to request a specific Difficulty object

        # Request: GET

        ## Parameters

        ### Query parameters

        - difficulty_id: the id of the difficulty

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a DifficultySerializer object

        ## Cache:

        - The requested difficulty object is not saved in the redis cache
        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a difficulty object is saved or deleted
        """
        return super().retrieve(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        An Api View which provides a method to create a Difficulty object

        # Request: POST

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a DifficultyCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a difficulty object is saved or deleted
        """
        return super().create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        An Api View which provides a method to update a specific Difficulty object

        # Request: PUT

        ## Parameters

        ### Query parameters

        - difficulty_id: the id of the difficulty

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a DifficultyCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a difficulty object is saved or deleted
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        An Api View which provides a method to partially_update a specific Difficulty object

        # Request: PATCH

        ## Parameters

        ### Query parameters

        - difficulty_id: the id of the difficulty

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a DifficultyCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a difficulty object is saved or deleted
        """
        return super().partial_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        An Api View which provides a method to delete a specific Difficulty object

        # Request: DELETE

        ## Parameters

        ### Query parameters

        - difficulty_id: the id of the difficulty

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        None

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a difficulty object is saved or deleted
        """
        return super().destroy(self, request, *args, **kwargs)
