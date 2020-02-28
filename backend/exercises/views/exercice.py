from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import permissions, generics

from exercises.models.exercise import Exercise
from exercises.serializers.exercise import ExerciseSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class ExerciseGetById(generics.RetrieveAPIView):
    """
      An Api View which provides a method to request a specific Exercise object

      # Request: GET

      ## Parameters

      ### Query parameters

      - exercise_id: the id of the exercise

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a ExerciseSerializer object

      ## Cache:

      - The requested exercise object is not saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a exercise object is saved
    """

    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_field = "id"
    lookup_url_kwarg = "exercise_id"

    def get_queryset(self):
        key = "exercises_all"
        if key in cache:
            return cache.get(key)
        else:
            exercises = Exercise.objects.all()
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises


class ExercisesAll(generics.ListAPIView):
    """
       An Api View which provides a method to request a list of Exercise objects

       # Request: GET

       ## Parameters

       None

       ## Permissions

       ### Token: Bearer

       - The user must be **authenticated**, so the given token must be valid

       ## Return

       - The return is a **List** of ExerciseSerializer objects

       ## Cache:

       - The list is saved in the redis cache if the key do not exist
       - Else return the list already saved in the cache
       - The cache is delete when a exercise object is saved
    """
    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        key = "exercises_all"
        if key in cache:
            return cache.get(key)
        else:
            exercises = Exercise.objects.all()
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises


class ExercisesAllFutureDueDate(ExercisesAll):
    """
       An Api View which provides a method to request a list of Exercise objects

       # Request: GET

       ## Parameters

       None

       ## Permissions

       ### Token: Bearer

       - The user must be **authenticated**, so the given token must be valid

       ## Return

       - The return is a **List** of ExerciseSerializer objects

       ## Cache:

       - The list is saved in the redis cache if the key do not exist
       - Else return the list already saved in the cache
       - The cache is delete when a exercise object is saved
    """
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllBySession(generics.ListAPIView):
    """
      An Api View which provides a method to request a list of Exercise objects related by a session

      # Request: GET

      ## Parameters

      ### Query parameters

      - session_id: the id of the session

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a ExerciseSerializer object

      ## Cache:

      - The requested list of exercise objects is saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a exercise object is saved
    """

    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "session_id"

    def get_queryset(self):
        key = "exercises_session_id_{id}".format(id=self.kwargs["session_id"])
        key_all = "exercises_all"
        if key in cache:
            return cache.get(key)
        elif key_all in cache:
            exercises_all = cache.get(key_all)
            exercises = exercises_all.filter(session__id=self.kwargs["session_id"])
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises
        else:
            exercises_all = Exercise.objects.all()
            cache.set(key_all, exercises_all, timeout=CACHE_TTL)
            exercises = exercises_all.filter(session__id=self.kwargs["session_id"])
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises

    def get_object(self):
        obj = self.filter_queryset(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllBySessionFutureDueDate(ExercisesAllBySession):
    """
      An Api View which provides a method to request a list of future Exercise objects related by a session

      # Request: GET

      ## Parameters

      ### Query parameters

      - session_id: the id of the session

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a ExerciseSerializer object

      ## Cache:

      - The requested list of exercise objects is saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a exercise object is saved
    """

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllBySection(generics.ListAPIView):
    """
      An Api View which provides a method to request a list of Exercise objects related by a section

      # Request: GET

      ## Parameters

      ### Query parameters

      - section_id: the id of the session

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a ExerciseSerializer object

      ## Cache:

      - The requested list of exercise objects is saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a exercise object is saved
    """

    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "section_id"

    def get_queryset(self):
        key = "exercises_section_id_{id}".format(id=self.kwargs["section_id"])
        key_all = "exercises_all"
        if key in cache:
            return cache.get(key)
        elif key_all in cache:
            exercises_all = cache.get(key_all)
            exercises = exercises_all.filter(section__id=self.kwargs["section_id"])
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises
        else:
            exercises_all = Exercise.objects.all()
            cache.set(key_all, exercises_all, timeout=CACHE_TTL)
            exercises = exercises_all.filter(section__id=self.kwargs["section_id"])
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises

    def get_object(self):
        obj = self.filter_queryset(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllBySectionFutureDueDate(ExercisesAllBySection):
    """
      An Api View which provides a method to request a list of future Exercise objects related by a section

      # Request: GET

      ## Parameters

      ### Query parameters

      - section_id: the id of the session

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a ExerciseSerializer object

      ## Cache:

      - The requested list of exercise objects is saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a exercise object is saved
    """

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllByCategory(generics.ListAPIView):
    """
      An Api View which provides a method to request a list of Exercise objects related by a category

      # Request: GET

      ## Parameters

      ### Query parameters

      - category_id: the id of the session

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a ExerciseSerializer object

      ## Cache:

      - The requested list of exercise objects is saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a exercise object is saved
    """

    serializer_class = ExerciseSerializer
    permission_classes = (permissions.IsAuthenticated,)
    lookup_url_kwarg = "category_id"

    def get_queryset(self):
        key = "exercises_category_id_{id}".format(id=self.kwargs["category_id"])
        key_all = "exercises_all"
        if key in cache:
            return cache.get(key)
        elif key_all in cache:
            exercises_all = cache.get(key_all)
            exercises = exercises_all.filter(category__id=self.kwargs["category_id"])
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises
        else:
            exercises_all = Exercise.objects.all()
            cache.set(key_all, exercises_all, timeout=CACHE_TTL)
            exercises = exercises_all.filter(category__id=self.kwargs["category_id"])
            cache.set(key, exercises, timeout=CACHE_TTL)
            return exercises

    def get_object(self):
        obj = self.filter_queryset(self.get_queryset())
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllByCategoryFutureDueDate(ExercisesAllByCategory):
    """
      An Api View which provides a method to request a list of future Exercise objects related by a category

      # Request: GET

      ## Parameters

      ### Query parameters

      - category_id: the id of the session

      ## Permissions

      ### Token: Bearer

      - The user must be **authenticated**, so the given token must be valid

      ## Return

      - The return is a ExerciseSerializer object

      ## Cache:

      - The requested list of exercise objects is saved in the redis cache
      - The list, used for the lookup, is saved in the redis cache if the key do not exist
      - Else return the object from the list already saved in the cache
      - The cache is delete when a exercise object is saved
    """

    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj
