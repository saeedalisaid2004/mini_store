from django.urls import path

from orders.apis import (
    ChangeOrderStatusAPI,
    CheckoutAPI,
    OrderDetailAPI,
    OrderListAPI,
)

app_name = "orders"

urlpatterns = [
    path("checkout/", CheckoutAPI.as_view(), name="checkout"),
    path("orders/", OrderListAPI.as_view(), name="order-list"),
    path("orders/<int:order_id>/", OrderDetailAPI.as_view(), name="order-detail"),
    path(
        "orders/<int:order_id>/status/",
        ChangeOrderStatusAPI.as_view(),
        name="change-order-status",
    ),
]
