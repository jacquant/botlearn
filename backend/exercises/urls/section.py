from django.urls import path

from exercises.views.section import SectionAll, SectionGetById


urlpatterns = [
    # /api/sections/all/
    path("all/", SectionAll.as_view(), name="sections_all"),
    # /api/sections/get/{section_id}
    path("get/<int:section_id>", SectionGetById.as_view(), name="section_get"),
]
