from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.section import Section
from exercises.serializers.section import SectionSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class SectionAll(generics.ListAPIView):
    """
    An Api View which provides a method to request a list of Section objects

    # Request: GET

    ## Parameters

    None

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a **List** of SectionSerializer objects

    ## Cache:

    - The list is saved in the redis cache if the key do not exist
    - Else return the list already saved in the cache
    - The cache is delete when a section object is saved
    """
    serializer_class = SectionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = "sections_all"
        if key in cache:
            return cache.get(key)
        else:
            sections = Section.objects.all()
            cache.set(key, sections, timeout=CACHE_TTL)
            return sections


class SectionGetById(generics.RetrieveAPIView):
    """
    An Api View which provides a method to request a specific Section object

    # Request: GET

    ## Parameters

    ### Query parameters

    - section_id: the id of the difficulty

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a SectionSerializer object

    ## Cache:

    - The requested section object is not saved in the redis cache
    - The list, used for the lookup, is saved in the redis cache if the key do not exist
    - Else return the object from the list already saved in the cache
    - The cache is delete when a section object is saved
    """
    serializer_class = SectionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "section_id"
    lookup_field = "id"

    def get_queryset(self):
        key = "sections_all"
        if key in cache:
            return cache.get(key)
        else:
            sections = Section.objects.all()
            cache.set(key, sections, timeout=CACHE_TTL)
            return sections
