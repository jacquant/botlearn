from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import permissions, viewsets

from exercises.models.target_students import TargetStudents
from exercises.serializers.target_students import (
    TargetStudentsSerializer,
    TargetStudentsCUDSerializer,
)

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class TargetStudentsViewSet(viewsets.ModelViewSet):
    lookup_url_kwarg = "target_students_id"
    lookup_field = "id"

    def get_queryset(self):
        key = "target_students_all"
        if key in cache:
            return cache.get(key)
        else:
            target_students = TargetStudents.objects.all()
            cache.set(key, target_students, timeout=CACHE_TTL)
            return target_students

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["list", "retrieve"]:
            permission_classes = [permissions.IsAuthenticated]
        else:
            permission_classes = [permissions.IsAdminUser]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action in ["list", "retrieve"]:
            return TargetStudentsSerializer
        else:
            return TargetStudentsCUDSerializer

    def list(self, request, *args, **kwargs):
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
        - The cache is delete when a target_students object is saved or deleted
        """
        return super().list(self, request, *args, **kwargs)

    def retrieve(self, request, *args, **kwargs):
        """
        An Api View which provides a method to request a specific TargetStudents object

        # Request: GET

        ## Parameters

        ### Query parameters

        - target_students_id: the id of the target_students

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid

        ## Return

        - The return is a TargetStudentsSerializer object

        ## Cache:

        - The requested target_students object is not saved in the redis cache
        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a target_students object is saved or deleted
        """
        return super().retrieve(self, request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        """
        An Api View which provides a method to create a TargetStudents object

        # Request: POST

        ## Parameters

        None

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a TargetStudentsCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a target_students object is saved or deleted
        """
        return super().create(self, request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        """
        An Api View which provides a method to update a specific TargetStudents object

        # Request: PUT

        ## Parameters

        ### Query parameters

        - target_students_id: the id of the target_students

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a TargetStudentsCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a target_students object is saved or deleted
        """
        return super().update(self, request, *args, **kwargs)

    def partial_update(self, request, *args, **kwargs):
        """
        An Api View which provides a method to partially_update a specific TargetStudents object

        # Request: PATCH

        ## Parameters

        ### Query parameters

        - target_students_id: the id of the target_students

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        - The return is a TargetStudentsCUDSerializer object

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a target_students object is saved or deleted
        """
        return super().partial_update(self, request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        """
        An Api View which provides a method to delete a specific TargetStudents object

        # Request: DELETE

        ## Parameters

        ### Query parameters

        - target_students_id: the id of the targets_student

        ## Permissions

        ### Token: Bearer

        - The user must be **authenticated**, so the given token must be valid
        - The user must be an AdminUser

        ## Return

        None

        ## Cache:

        - The list, used for the lookup, is saved in the redis cache if the key do not exist
        - Else return the object from the list already saved in the cache
        - The cache is delete when a target_students object is saved or deleted
        """
        return super().destroy(self, request, *args, **kwargs)
