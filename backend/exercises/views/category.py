from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.category import Category
from exercises.serializers.category import CategorySerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class CategoryAll(generics.ListAPIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = "categories_all"
        if key in cache:
            return cache.get(key)
        else:
            categories = Category.objects.all()
            cache.set(key, categories, timeout=CACHE_TTL)
            return categories


class CategoryGetById(generics.RetrieveAPIView):
    serializer_class = CategorySerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "category_id"
    lookup_field = "id"

    def get_queryset(self):
        key = "categories_all"
        if key in cache:
            return cache.get(key)
        else:
            categories = Category.objects.all()
            cache.set(key, categories, timeout=CACHE_TTL)
            return categories
