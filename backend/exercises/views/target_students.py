from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.target_students import TargetStudents
from exercises.serializers.target_students import TargetStudentsSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class TargetStudentsAll(generics.ListAPIView):
    serializer_class = TargetStudentsSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = "target_students_all"
        if key in cache:
            return cache.get(key)
        else:
            targets_students = TargetStudents.objects.all()
            cache.set(key, targets_students, timeout=CACHE_TTL)
            return targets_students


class TargetStudentsGetById(generics.RetrieveAPIView):
    serializer_class = TargetStudentsSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "target_students_id"
    lookup_field = "id"

    def get_queryset(self):
        key = "target_students_all"
        if key in cache:
            return cache.get(key)
        else:
            targets_students = TargetStudents.objects.all()
            cache.set(key, targets_students, timeout=CACHE_TTL)
            return targets_students
