from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.generics import ListAPIView

from exercises.models import Session
from exercises.serializers.admin import SessionMinimalSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class AdminView(ListAPIView):
    permission_classes = [permissions.IsAdminUser]
    serializer_class = SessionMinimalSerializer

    def get_queryset(self):
        """Return the query of objects needed for the lookups and the api."""
        key = "sessions_all"
        if key in cache:
            return cache.get(key)
        sessions = Session.objects.all()
        cache.set(key, sessions, timeout=CACHE_TTL)
        return sessions
