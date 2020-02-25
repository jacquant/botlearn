from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.tag import Tag
from exercises.serializers.tag import TagSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class TagAll(generics.ListAPIView):
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
