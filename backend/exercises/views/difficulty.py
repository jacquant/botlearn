from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.difficulty import Difficulty
from exercises.serializers.difficulty import DifficultySerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class DifficultyAll(generics.ListAPIView):
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
