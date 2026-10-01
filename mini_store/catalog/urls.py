from django.urls import path

from catalog.apis import (
    ProductDetailAPI,
    ProductListAPI,
)  # أو من catalog.views حسب مكان الـ APIs عندك

urlpatterns = [
    path("", ProductListAPI.as_view(), name="product-list"),
    path("<int:pk>/", ProductDetailAPI.as_view(), name="product-detail"),
]
