from django.urls import path
from . import apis

urlpatterns = [
    path("products/", apis.ProductListAPI.as_view(), name="product-list"),
    path(
        "products/<int:product_id>/",
        apis.ProductDetailAPI.as_view(),
        name="product-detail",
    ),
]
