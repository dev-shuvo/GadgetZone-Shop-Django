from django.urls import path
from .views import *

urlpatterns = [
    path("", cart, name="cart"),
    path("add_to_cart/<int:product_id>/", add_to_cart, name="add_to_cart"),
    path("minus_from_cart/<int:product_id>/", minus_from_cart, name="minus_from_cart"),
    path(
        "delete_cart_item/<int:product_id>/,<int:cart_item_id>/",
        delete_cart_item,
        name="delete_cart_item",
    ),
    path("checkout/", checkout, name="checkout"),
]
