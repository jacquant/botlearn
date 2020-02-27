from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.difficulty import Difficulty
from exercises.serializers.difficulty import DifficultySerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class DifficultyAll(generics.ListAPIView):
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
    - The cache is delete when a difficulty object is saved
    """
    serializer_class = DifficultySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = "difficulties_all"
        if key in cache:
            return cache.get(key)
        else:
            difficulties = Difficulty.objects.all()
            cache.set(key, difficulties, timeout=CACHE_TTL)
            return difficulties


class DifficultyGetById(generics.ListAPIView):
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
    - The cache is delete when a difficulty object is saved
    """
    serializer_class = DifficultySerializer
    permission_classes = (permissions.IsAuthenticated,)
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
