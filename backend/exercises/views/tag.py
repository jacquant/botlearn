from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.tag import Tag
from exercises.serializers.tag import TagSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class TagAll(generics.ListAPIView):
    """
    An Api View which provides a method to request a list of Tag objects

    # Request: GET

    ## Parameters

    None

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a **List** of TagSerializer objects

    ## Cache:

    - The list is saved in the redis cache if the key do not exist
    - Else return the list already saved in the cache
    - The cache is delete when a tag object is saved
    """
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = "tags_all"
        if key in cache:
            return cache.get(key)
        else:
            tags = Tag.objects.all()
            cache.set(key, tags, timeout=CACHE_TTL)
            return tags


class TagGetById(generics.RetrieveAPIView):
    """
    An Api View which provides a method to request a specific Tag object

    # Request: GET

    ## Parameters

    ### Query parameters

    - tag_id: the id of the tag

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a TagSerializer object

    ## Cache:

    - The requested tag object is not saved in the redis cache
    - The list, used for the lookup, is saved in the redis cache if the key do not exist
    - Else return the object from the list already saved in the cache
    - The cache is delete when a section object is saved
    """
    serializer_class = TagSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "tag_id"
    lookup_field = "id"

    def get_queryset(self):
        key = "tags_all"
        if key in cache:
            return cache.get(key)
        else:
            tags = Tag.objects.all()
            cache.set(key, tags, timeout=CACHE_TTL)
            return tags
