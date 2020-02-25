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
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllBySession(generics.ListAPIView):
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
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllBySection(generics.ListAPIView):
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
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj


class ExercisesAllByCategory(generics.ListAPIView):
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
    def get_object(self):
        queryset = self.filter_queryset(self.get_queryset())
        filter_kwargs = {"due_date__date__lte": timezone.now()}
        obj = get_object_or_404(queryset, **filter_kwargs)

        # May raise a permission denied
        self.check_object_permissions(self.request, obj)
        return obj