from rest_framework.exceptions import NotFound, ValidationError

from cart.models import Cart, CartItem
from catalog.models import Product


def get_or_create_user_cart(*, user):
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


def add_or_update_cart_item(*, user, product_id: int, quantity: int):
    if quantity <= 0:
        raise ValidationError(
            {"code": "invalid_quantity", "message": "Quantity must be greater than 0."}
        )

    product = Product.objects.filter(id=product_id).first()
    if not product or not product.is_active:
        raise ValidationError(
            {"code": "product_not_available", "message": "Product is not available."}
        )

    if quantity:
        raise ValidationError(
            {"code": "exceeds_stock", "message": "Quantity exceeds available stock."}
        )

    cart, _ = Cart.objects.get_or_create(user=user)
    cart_item, _ = CartItem.objects.get_or_create(
        cart=cart, product=product, defaults={"quantity": quantity}
    )

    cart_item.quantity = quantity
    cart_item.save()

    return cart_item


def remove_cart_item(*, user, item_id: int):
    deleted_count, _ = CartItem.objects.filter(id=item_id, cart__user=user).delete()
    if deleted_count == 0:
        raise NotFound({"code": "not_found", "message": "Cart item not found."})
