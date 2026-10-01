from rest_framework.exceptions import NotFound
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.views import APIView

from catalog.selectors import get_product_by_id, get_products
from catalog.serializers import ProductSerializer


class ProductListAPI(APIView):
    def get(self, request):
        accept_lang = request.headers.get("Accept-Language", "ar")
        lang = "en" if "en" in accept_lang else "ar"

        category = request.query_params.get("category")
        search = request.query_params.get("search")
        ordering = request.query_params.get("ordering")

        products = get_products(
            lang=lang, category_slug=category, search=search, ordering=ordering
        )

        paginator = PageNumberPagination()
        paginated_products = paginator.paginate_queryset(products, request, view=self)

        if paginated_products is not None:
            serializer = ProductSerializer(
                paginated_products, many=True, context={"lang": lang}
            )
            return paginator.get_paginated_response(serializer.data)

        serializer = ProductSerializer(products, many=True, context={"lang": lang})
        return Response(serializer.data)


class ProductDetailAPI(APIView):
    def get(self, request, product_id: int):
        accept_lang = request.headers.get("Accept-Language", "ar")
        lang = "en" if "en" in accept_lang else "ar"

        product = get_product_by_id(product_id=product_id)
        if not product:
            raise NotFound({"code": "not_found", "message": "Product not found."})

        serializer = ProductSerializer(product, context={"lang": lang})
        return Response(serializer.data)
