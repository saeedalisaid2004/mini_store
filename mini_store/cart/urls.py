from django.urls import path
from .apis import CartAPI, CartItemDetailAPI

urlpatterns = [
    path("", CartAPI.as_view(), name="cart-detail"),
    path("items/<int:item_id>/", CartItemDetailAPI.as_view(), name="cart-item-detail"),
]
