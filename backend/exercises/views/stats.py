from django.conf import settings
from django.core.cache import cache
from django.core.cache.backends.base import DEFAULT_TIMEOUT

from rest_framework import (
    generics,
    permissions,
)

from exercises.models.submission import Submission
from exercises.serializers.stats import StatSerializer

CACHE_TTL = getattr(settings, "CACHE_TTL", DEFAULT_TIMEOUT)


class BaseErrorBy(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    lookup_url_kwarg = "field_id"
    lookup_field = "exercise__model__id"

    serializer_class = StatSerializer

    def get_queryset(self):
        key = "submissions_all"
        if key in cache:
            return cache.get(key)
        else:
            submissions = Submission.objects.all()
            cache.set(key, submissions, timeout=CACHE_TTL)
        return submissions


    def get_object(self):
        filter_kwargs = {self.lookup_field: self.kwargs[self.lookup_url_kwarg]}
        queryset = (
            self.get_queryset()
            .filter(**filter_kwargs)
            .order_by("-submission_date")
        )
        errors = [
            error_tuple
            for error_tuple in queryset.values_list(
                "id", "errors__error__code", "errors__error__message", "errors__error__type_error", "errors__counter"
            )
            if error_tuple[1:] != (None, None, None, None)
        ]
        count = {}
        for id_submission, error_code, error_message, error_type, error_counter in errors:
            if error_code in count:
                count[error_code]["counter"] += error_counter
            else:
                count[error_code] = {
                    "counter": error_counter,
                    "message": error_message,
                    "type": error_type,
                    "submissions_list": [],
                }
            count[error_code]["submissions_list"].append(id_submission)
        errors = [
            {**error_data, "code": code} for code, error_data in count.items()
        ]
        return {"number_submissions": len(queryset), "errors": errors}


class ErrorsBySection(BaseErrorBy):
    lookup_url_kwarg = "section_id"
    lookup_field = "exercise__section__id"


class ErrorsBySession(BaseErrorBy):
    lookup_url_kwarg = "session_id"
    lookup_field = "exercise__session__id"


class ErrorsByAuthor(BaseErrorBy):
    lookup_url_kwarg = "author_mail"
    lookup_field = "author__mail"


class ErrorsByExercise(BaseErrorBy):
    lookup_url_kwarg = "exercise_id"
    lookup_field = "exercise__id"


class ErrorsByExerciseFinal(BaseErrorBy):
    lookup_url_kwarg = "exercise_id"
    lookup_field = "exercise__id"

    def get_queryset(self):
        key = "submissions_all"
        if key in cache:
            return cache.get(key).filter(final=True)
        else:
            submissions = Submission.objects.all()
            cache.set(key, submissions, timeout=CACHE_TTL)
            return submissions.filter(final=True)
