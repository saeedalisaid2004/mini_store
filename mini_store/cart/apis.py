from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.selectors import get_user_cart
from cart.serializers import AddToCartSerializer, CartSerializer
from cart.services import add_or_update_cart_item, remove_cart_item


class CartAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        accept_lang = request.headers.get("Accept-Language", "ar")
        lang = "en" if "en" in accept_lang else "ar"

        cart = get_user_cart(user=request.user)
        serializer = CartSerializer(cart, context={"lang": lang})
        return Response(serializer.data)

    def post(self, request):
        serializer = AddToCartSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        add_or_update_cart_item(
            user=request.user,
            product_id=serializer.validated_data["product_id"],
            quantity=serializer.validated_data["quantity"],
        )
        return Response(
            {"message": "Item added to cart successfully"},
            status=status.HTTP_200_OK,
        )


class CartItemDetailAPI(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def delete(self, request, item_id: int):
        remove_cart_item(user=request.user, item_id=item_id)
        return Response(status=status.HTTP_204_NO_CONTENT)
