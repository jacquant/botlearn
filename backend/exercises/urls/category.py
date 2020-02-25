from django.urls import path

from exercises.views.category import CategoryAll, CategoryGetById


urlpatterns = [
    # /api/categories/all/
    path("all/", CategoryAll.as_view(), name="categories_all"),
    # /api/categories/get/{category_id}
    path("get/<int:category_id>", CategoryGetById.as_view(), name="category_get"),
]
