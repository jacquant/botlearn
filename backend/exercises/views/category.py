from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.category import Category
from exercises.serializers.category import CategorySerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class CategoryAll(generics.ListAPIView):
    """
    An Api View which provides a method to request a list of Category objects

    # Request: GET

    ## Parameters

    None

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a **List** of CategorySerializer objects

    ## Cache:

    - The list is saved in the redis cache if the key do not exist
    - Else return the list already saved in the cache
    - The cache is delete when a category object is saved
    """
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
    """
    An Api View which provides a method to request a specific Category object

    # Request: GET

    ## Parameters

    ### Query parameters

    - category_id: the id of the category

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a CategorySerializer object

    ## Cache:

    - The requested category object is not saved in the redis cache
    - The list, used for the lookup, is saved in the redis cache if the key do not exist
    - Else return the object from the list already saved in the cache
    - The cache is delete when a category object is saved
    """
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
