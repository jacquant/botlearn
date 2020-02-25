from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.section import Section
from exercises.serializers.section import SectionSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class SectionAll(generics.ListAPIView):
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
