from django.core.exceptions import ValidationError
from rest_framework import status
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from cart.selectors import get_user_cart
from orders.models import Order
from orders.selectors import get_user_order_detail, get_user_orders
from orders.serializers import OrderDetailSerializer
from orders.services import change_order_status, checkout_cart


class CheckoutAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        cart = get_user_cart(user=request.user)
        if not cart or not cart.items.exists():
            return Response(
                {"error": {"code": "CART_EMPTY", "message": "السلة فارغة"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        idempotency_key = request.headers.get("Idempotency-Key")

        try:
            order = checkout_cart(
                user=request.user, cart=cart, idempotency_key=idempotency_key
            )
        except ValidationError as e:
            return Response(
                {"error": {"code": "CHECKOUT_ERROR", "message": str(e)}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class OrderListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = get_user_orders(user=request.user)
        serializer = OrderDetailSerializer(orders, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class OrderDetailAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        order = get_user_order_detail(user=request.user, order_id=order_id)
        if not order:
            return Response(
                {"error": {"code": "NOT_FOUND", "message": "الطلب غير موجود"}},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = OrderDetailSerializer(order)
        return Response(serializer.data, status=status.HTTP_200_OK)


class ChangeOrderStatusAPI(APIView):
    permission_classes = [IsAdminUser]

    def patch(self, request, order_id):
        new_status = request.data.get("status")
        if not new_status:
            return Response(
                {"error": {"code": "INVALID_STATUS", "message": "الحالة مطلوبة"}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            return Response(
                {"error": {"code": "NOT_FOUND", "message": "الطلب غير موجود"}},
                status=status.HTTP_404_NOT_FOUND,
            )

        try:
            updated_order = change_order_status(order=order, new_status=new_status)
        except ValidationError as e:
            return Response(
                {"error": {"code": "INVALID_TRANSITION", "message": str(e)}},
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer = OrderDetailSerializer(updated_order)
        return Response(serializer.data, status=status.HTTP_200_OK)
