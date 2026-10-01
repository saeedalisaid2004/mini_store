from decimal import Decimal

from rest_framework import serializers

from cart.models import Cart, CartItem
from catalog.serializers import ProductSerializer


class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = CartItem
        fields = ("id", "product", "quantity", "subtotal")

    def get_subtotal(self, obj: CartItem) -> Decimal:
        return obj.product.price * obj.quantity


class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ("id", "items", "total")

    def get_total(self, obj: Cart) -> Decimal:
        return sum(
            (item.product.price * item.quantity for item in obj.items.all()),
            Decimal("0.00"),
        )


class AddToCartSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(default=1)
