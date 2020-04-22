from django.core.cache import cache

from rest_framework import (
    generics,
    permissions,
)

from exercises.models.submission import Submission
from exercises.serializers.stats import StatSerializer


class BaseErrorBy(generics.RetrieveAPIView):
    permission_classes = (permissions.IsAdminUser,)
    lookup_url_kwarg = "field_id"
    lookup_field = "exercise__model__id"
    serializer_class = StatSerializer

    def get_queryset(self):
        key = "submissions_all"
        if key in cache:
            return cache.get(key)
        return Submission.objects.all()

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
                "id", "errors__error__code", "errors__counter"
            )
            if error_tuple[1:] != (None, None)
        ]
        count = {}
        for id_submission, error_code, error_counter in errors:
            if error_code in count:
                count[error_code]["counter"] += error_counter
            else:
                count[error_code] = {
                    "counter": error_counter,
                    "submissions_list": [],
                }
            count[error_code]["submissions_list"].append(id_submission)
        return {"number_submissions": len(queryset), "errors": count}


class ErrorsBySection(BaseErrorBy):
    lookup_url_kwarg = "section_id"
    lookup_field = "exercise__section__id"


class ErrorsBySession(BaseErrorBy):
    lookup_url_kwarg = "session_id"
    lookup_field = "exercise__session__id"


class ErrorsByExercise(BaseErrorBy):
    lookup_url_kwarg = "exercise_id"
    lookup_field = "exercise__id"
