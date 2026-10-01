from django.urls import path

from cart.apis import CartAPI, CartItemDetailAPI

urlpatterns = [
    path("", CartAPI.as_view(), name="cart-detail"),
    path("items/<int:pk>/", CartItemDetailAPI.as_view(), name="cart-item-detail"),
]
