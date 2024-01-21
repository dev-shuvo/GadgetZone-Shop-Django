from django.urls import path
from .views import *

urlpatterns = [
    path("", store, name="store"),
    path("category/<slug:category_slug>/", store, name="products_by_category"),
    path(
        "category/<slug:category_slug>/<slug:product_slug>/",
        product_details,
        name="product_details",
    ),
    path("search/", search, name="search"),
    path("submit-review/<int:product_id>/", submit_review, name="submit_review"),
]
