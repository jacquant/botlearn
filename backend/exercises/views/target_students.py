from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, generics

from exercises.models.target_students import TargetStudents
from exercises.serializers.target_students import TargetStudentsSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class TargetStudentsAll(generics.ListAPIView):
    """
    An Api View which provides a method to request a list of TargetStudents objects

    # Request: GET

    ## Parameters

    None

    ## Permissions

    ### Token: Bearer

    - The user must be **authenticated**, so the given token must be valid

    ## Return

    - The return is a **List** of TargetStudentsSerializer objects

    ## Cache:

    - The list is saved in the redis cache if the key do not exist
    - Else return the list already saved in the cache
    - The cache is delete when a target student object is saved
    """
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
    """
      An Api View which provides a method to request a specific TargetStudent object

      # Request: GET

      ## Parameters

      ### Query parameters

      - target_students_id: the id of the target student

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a TargetStudentsSerializer object

      ## Cache:

      - The requested target students object is not saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a target students object is saved
      """
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
