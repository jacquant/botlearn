from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import (
    include,
    path,
    re_path,
)

from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import (
    permissions,
    routers,
)

from memoire.settings import BACK_URL


admin.site.site_header = "Admin - Site pour le mémoire"
admin.site.site_title = "Site mémoire"
urlpatterns = [
    path("jet", include("jet.urls", "jet")),
    path("admin/", admin.site.urls),
    path(
        "api/password_reset/",
        include("django_rest_passwordreset.urls", namespace="password_reset"),
    ),
    path("api/", include("accounts.urls")),
    path("api/", include("exercises.urls")),
    path("api/", include("bot.urls")),
    path("api/code/", include("sandbox.urls")),
]

if settings.DEBUG:
    router = routers.DefaultRouter()
    # Configuration du Swagger=documentation de l'API
    schema_view = get_schema_view(
        openapi.Info(
            title="MEMOIRE API",
            default_version="v2020.04.22",
            description="Api de développement pour le memoire",
            terms_of_service="",
            contact=openapi.Contact(email="antoine.jacques@student.unamur.be"),
            license=openapi.License(name="Apache Licence 2.0"),
        ),
        url=BACK_URL,
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    # En mode debug, les fichiers statics et media sont servis par le serveur
    # django, à ne pas faire en production
    # (performance)!
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(
        settings.MEDIA_URL, document_root=settings.MEDIA_ROOT
    )
    # Tous les points d'API nécessaires à l'API en version documentées
    urlpatterns += [
        re_path("^", include(router.urls)),
        re_path(
            r"^swagger(?P<format>\.json|\.yaml)$",
            schema_view.without_ui(cache_timeout=0),
            name="schema-json",
        ),
        re_path(
            r"^api-doc/$",
            schema_view.with_ui("swagger", cache_timeout=0),
            name="schema-swagger-ui",
        ),
        re_path(
            r"^redoc/$",
            schema_view.with_ui("redoc", cache_timeout=0),
            name="schema-redoc",
        ),
        re_path(
            r"^api-auth/",
            include("rest_framework.urls", namespace="rest_framework"),
        ),
    ]
