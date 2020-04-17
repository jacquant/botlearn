from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import (
    permissions,
    viewsets,
)

from exercises.models.error import Error
from exercises.serializers.error import (
    ErrorCUDSerializer,
    ErrorSerializer,
)


CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class ActionsErrorView(viewsets.ModelViewSet):
    """Define actions in the views and documents its for the api doc view."""

    def list(self, request, *args, **kwargs):
        """Provides a method to request a list of Error objects.

        # Request: GET

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

         ## Return

        - The return is a **List** of ErrorSerializer objects

        ## Cache:

        - The list is saved in the redis cache if the key do not exist
        - Else return the list already saved in the cache
        - The cache is delete when a error object is saved or deleted
        """
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """Provides a method to request a specific Error object.

        # Request: GET

        ## Parameters

        ### Query parameters

        - error_id: the id of the error

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a ErrorSerializer object

        ## Cache:

        - The requested error object is not saved in the redis cache
        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error object is saved or deleted
        """
        return super().retrieve(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """An Api View which provides a method to create a Error object.

        # Request: POST

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a ErrorCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error object is saved or deleted
        """
        return super().create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """Provides a method to update a specific Error object.

        # Request: PUT

        ## Parameters

        ### Query parameters

        - error_id: the id of the error

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a ErrorCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error object is saved or deleted
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """Provides a method to partially_update a specific Error object.

        # Request: PATCH

        ## Parameters

        ### Query parameters

        - error_id: the id of the error

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a ErrorCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the
          key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a error object is saved or deleted
        """
        return super().partial_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """Provides a method to delete a specific Error object.

        # Request: DELETE

        ## Parameters

        ### Query parameters

        - error_id: the id of the error

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
        - The cache is delete when a error object is saved or deleted
        """
        return super().destroy(self, request, *args, **kwargs)


class ErrorViewSet(ActionsErrorView):
    """ViewSet uses for the Error objects."""

    lookup_url_kwarg = "error_id"
    lookup_field = "id"

    def get_queryset(self):
        """Return the query of objects needed for the lookups and the api."""
        key = "errors_all"
        if key in cache:
            return cache.get(key)
        errors = Error.objects.all()
        cache.set(key, errors, timeout=CACHE_TTL)
        return errors

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
            return ErrorSerializer
        return ErrorCUDSerializer
