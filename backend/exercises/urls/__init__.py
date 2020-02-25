from django.urls import include, path

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
    path("sections/", include("exercises.urls.section"))
]
