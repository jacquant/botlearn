from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, generics

from exercises.models.session import Session
from exercises.serializers.session import SessionSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class SessionGetById(generics.RetrieveAPIView):
    """
    An Api View which provides a method to request a specific Session object

    # Request: GET

    ## Parameters

    ### Query parameters

    - session_id: the id of the difficulty

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a SessionSerializer object

    ## Cache:

    - The requested session object is not saved in the redis cache
    - The list, used for the lookup, is saved in the redis cache if the key do not exist
    - Else return the object from the list already saved in the cache
    - The cache is delete when a session object is saved
    """

    serializer_class = SessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"
    lookup_url_kwarg = "session_id"

    def get_queryset(self):
        key = "sessions_all"
        if key in cache:
            return cache.get(key)
        else:
            sessions = Session.objects.all()
            cache.set(key, sessions, timeout=CACHE_TTL)
            return sessions


class SessionAll(generics.ListAPIView):
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
    - The cache is delete when a session object is saved
    """
    serializer_class = SessionSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = "sessions_all"
        if key in cache:
            return cache.get(key)
        else:
            sessions = Session.objects.all()
            cache.set(key, sessions, timeout=CACHE_TTL)
            return sessions


class SessionAllFutureDate(SessionAll):
    """
    An Api View which provides a method to request a list of Session objects that comes in the future

    # Request: GET

    ## Parameters

    None

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a **List** of SessionSerializer objects

    ## Cache:

    - The requested session object is not saved in the redis cache
    - The list, used for the lookup, is saved in the redis cache if the key do not exist
    - Else return the object from the list already saved in the cache
    - The cache is delete when a session object is saved
    """

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class SessionAllByTarget(generics.ListAPIView):
    """
    An Api View which provides a method to request a list of Session objects for a specific target_students

    # Request: GET

    ## Parameters

    ### Query parameters

    - target_students_id: the id of the targeted students

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a **List** of SessionSerializer objects

    ## Cache:

    - The requested session object is saved in the redis cache
    - The list of all session, used for the lookup, is also saved in the redis cache if the key do not exist
    - Else return the object from the list already saved in the cache
    - The two levels cache is delete when a session object is saved
    """

    serializer_class = SessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "target_students_id"

    def get_queryset(self):
        key = "sessions_target_id_{id}".format(id=self.kwargs["target_students_id"])
        key_all = "sessions_all"
        if key in cache:
            return cache.get(key)
        elif key_all in cache:
            sessions_all = cache.get(key_all)
            sessions = sessions_all.filter(target__id=self.kwargs["target_students_id"])
            cache.set(key, sessions, timeout=CACHE_TTL)
            return sessions
        else:
            sessions_all = Session.objects.all()
            cache.set(key_all, sessions_all, timeout=CACHE_TTL)
            sessions = sessions_all.filter(target__id=self.kwargs["target_students_id"])
            cache.set(key, sessions, timeout=CACHE_TTL)
            return sessions

    def get_object(self):
        obj = self.filter_queryset(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj


class SessionAllByTargetFutureDate(SessionAllByTarget):
    """
    An Api View which provides a method to request a list of future Session objects for a specific target_students

    # Request: GET

    ## Parameters

    ### Query parameters

    - target_students_id: the id of the targeted students

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a **List** of SessionSerializer objects

    ## Cache:

    - The requested session object is saved in the redis cache
    - The list of all session, used for the lookup, is also saved in the redis cache if the key do not exist
    - Else return the object from the list already saved in the cache
    - The two levels cache is delete when a session object is saved
    """

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
