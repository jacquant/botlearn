from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT
from rest_framework import serializers

from exercises.models import Session, Exercise, Submission

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


def get_submissions():
    key = "submissions_all"
    if key in cache:
        return cache.get(key)
    submissions = Submission.objects.all()
    cache.set(key, submissions, timeout=CACHE_TTL)
    return submissions


class ExerciseMinimalSerializer(serializers.ModelSerializer):
    total_submission = serializers.SerializerMethodField()
    final_submission = serializers.SerializerMethodField()

    class Meta(object):
        model = Exercise
        fields = ("id", "name", "session", "total_submission", "final_submission",)

    @staticmethod
    def get_total_submission(obj):
        submissions = get_submissions().filter(exercise_id=obj.id)
        return len(submissions)

    @staticmethod
    def get_final_submission(obj):
        submissions = get_submissions().filter(exercise_id=obj.id, final=True)
        return len(submissions)


class SessionMinimalSerializer(serializers.ModelSerializer):
    exercises = ExerciseMinimalSerializer(many=True)

    class Meta(object):
        model = Session
        fields = ("id", "name", "exercises",)
