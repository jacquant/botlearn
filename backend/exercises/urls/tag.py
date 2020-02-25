from django.urls import path

from exercises.views.tag import TagAll, TagGetById


urlpatterns = [
    # /api/tags/all/
    path("all/", TagAll.as_view(), name="tags_all"),
    # /api/tags/get/{tag_id}
    path("get/<int:tag_id>", TagGetById.as_view(), name="tag_get")

]
