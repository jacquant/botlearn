from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.db.models import Prefetch
from django_filters import rest_framework as filters
from rest_framework import permissions, viewsets

from accounts.models.user import User
from exercises.filters.session import SessionFilter
from exercises.models.session import Session
from exercises.serializers.session import SessionSerializer, SessionCUDSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class SessionViewSet(viewsets.ModelViewSet):
    lookup_url_kwarg = "session_id"
    lookup_field = "id"
    filter_backends = (filters.DjangoFilterBackend,)
    filterset_class = SessionFilter

    def get_queryset(self):
        key = "sessions_all"
        if key in cache:
            return cache.get(key)
        else:
            sessions = Session.objects.prefetch_related(
                "target",
                Prefetch(
                    "in_charge_persons",
                    queryset=User.objects.only("mail", "first_name", "last_name"),
                ),
            ).all()
            cache.set(key, sessions, timeout=CACHE_TTL)
            print(sessions)
            return sessions

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in [
            "list",
            "retrieve",
        ]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in [
            "list",
            "retrieve",
        ]:
            return SessionSerializer
        else:
            return SessionCUDSerializer

    def list(self, request, *args, **kwargs):
        """
        An Api View which provides a method to request a list of Session objects

        # Request: GET

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

         ## Return

        - The return is a **List** of SessionSerializer objects

        ## Cache:

        - The list is saved in the redis cache if the key do not exist
        - Else return the list already saved in the cache
        - The cache is delete when a session object is saved or deleted
        """
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        An Api View which provides a method to request a specific Session object

        # Request: GET

        ## Parameters

        ### Query parameters

        - session_id: the id of the session

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a SessionSerializer object

        ## Cache:

        - The requested session object is not saved in the redis cache
        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a session object is saved or deleted
        """
        return super().retrieve(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        An Api View which provides a method to create a Session object

        # Request: POST

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a SessionCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a session object is saved or deleted
        """
        return super().create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        An Api View which provides a method to update a specific Session object

        # Request: PUT

        ## Parameters

        ### Query parameters

        - session_id: the id of the session

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a SessionCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a session object is saved or deleted
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        An Api View which provides a method to partially_update a specific Session object

        # Request: PATCH

        ## Parameters

        ### Query parameters

        - session_id: the id of the session

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a SessionCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a session object is saved or deleted
        """
        return super().partial_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        An Api View which provides a method to delete a specific Session object

        # Request: DELETE

        ## Parameters

        ### Query parameters

        - session_id: the id of the session

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        None

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a session object is saved or deleted
        """
        return super().destroy(self, request, *args, **kwargs)
