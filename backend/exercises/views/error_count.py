from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import (
    permissions,
    viewsets,
)

from exercises.models.error_count import ErrorCount
from exercises.serializers.error_count import (
    ErrorCountCUDSerializer,
    ErrorCountSerializer,
)


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class ActionsErrorCountView(viewsets.ModelViewSet):
    """Define actions in the views and documents its for the api doc view."""

    def list(self, request, *args, **kwargs):
        """Provides a method to request a list of ErrorCount objects.

        # Request: GET

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

         ## Return

        - The return is a **List** of ErrorCountSerializer objects

        ## Cache:

        - The list is saved in the redis cache if the key do not exist
        - Else return the list already saved in the cache
        - The cache is delete when a error_count object is saved or deleted
        """
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Provides a method to request a specific ErrorCount object.

        # Request: GET

        ## Parameters

        ### Query parameters

        - error_count_id: the id of the error_count

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a ErrorCountSerializer object

        ## Cache:

        - The requested error_count object is not saved in the redis cache
        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error_count object is saved or deleted
        """
        return super().retrieve(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """An Api View which provides a method to create a ErrorCount object.

        # Request: POST

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a ErrorCountCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error_count object is saved or deleted
        """
        return super().create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Provides a method to update a specific ErrorCount object.

        # Request: PUT

        ## Parameters

        ### Query parameters

        - error_count_id: the id of the error_count

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a ErrorCountCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error_count object is saved or deleted
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Provides a method to partially_update a specific ErrorCount object.

        # Request: PATCH

        ## Parameters

        ### Query parameters

        - error_count_id: the id of the error_count

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a ErrorCountCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error_count object is saved or deleted
        """
        return super().partial_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Provides a method to delete a specific ErrorCount object.

        # Request: DELETE

        ## Parameters

        ### Query parameters

        - error_count_id: the id of the error_count

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        None

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error_count object is saved or deleted
        """
        return super().destroy(self, request, *args, **kwargs)


class ErrorCountViewSet(ActionsErrorCountView):
    """ViewSet uses for the ErrorCount objects."""

    lookup_url_kwarg = "error_count_id"
    lookup_field = "id"

    def get_queryset(self):
        """Return the query of objects needed for the lookups and the api."""
        key = "errors_count_all"
        if key in cache:
            return cache.get(key)
        errors_count = ErrorCount.objects.all()
        cache.set(key, errors_count, timeout=CACHE_TTL)
        return errors_count

    def get_permissions(self):
        """Returns the list of permissions used by the view."""
        if self.action in {"list", "retrieve"}:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        """Method to return the serializer to use in function of the action."""
        if self.action in {"list", "retrieve"}:
            return ErrorCountSerializer
        return ErrorCountCUDSerializer
