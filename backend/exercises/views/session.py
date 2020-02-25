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
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class SessionAllByTarget(generics.ListAPIView):
    serializer_class = SessionSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "target_id"

    def get_queryset(self):
        key = "sessions_target_id_{id}".format(id=self.kwargs["target_id"])
        key_all = "sessions_all"
        if key in cache:
            return cache.get(key)
        elif key_all in cache:
            sessions_all = cache.get(key_all)
            sessions = sessions_all.filter(target__id=self.kwargs["target_id"])
            cache.set(key, sessions, timeout=CACHE_TTL)
            return sessions
        else:
            sessions_all = Session.objects.all()
            cache.set(key_all, sessions_all, timeout=CACHE_TTL)
            sessions = sessions_all.filter(target__id=self.kwargs["target_id"])
            cache.set(key, sessions, timeout=CACHE_TTL)
            return sessions

    def get_object(self):
        obj = self.filter_queryset(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj


class SessionAllByTargetFutureDate(SessionAllByTarget):
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
