from django.urls import (
    include,
    path,
)
from exercises.views.admin import AdminView

urlpatterns = [
    # /api/exercises/*
    path("exercises/", include("exercises.urls.exercise")),
    # /api/sessions/*
    path("sessions/", include("exercises.urls.session")),
    # /api/tags/*
    path("tags/", include("exercises.urls.tag")),
    # /api/target_students/*
    path("target_students/", include("exercises.urls.target_students")),
    # /api/categories/*
    path("categories/", include("exercises.urls.category")),
    # /api/difficulties/*
    path("difficulties/", include("exercises.urls.difficulty")),
    # /api/sections/*
    path("sections/", include("exercises.urls.section")),
    # /api/submissions/*
    path("submissions/", include("exercises.urls.submission")),
    # /api/errors/*
    path("errors/", include("exercises.urls.error")),
    # /api/errors_count/*
    path("errors_count/", include("exercises.urls.error_count")),
    # /api/stats/*
    path("stats/", include("exercises.urls.stats")),
    # /api/admin/
    path("admin/", AdminView.as_view())
]
