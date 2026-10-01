from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from catalog.models import Product
from orders.models import Order, OrderItem
from orders.tasks import send_order_confirmation_email


def checkout_cart(user, cart, idempotency_key=None):
    if idempotency_key:
        existing_order = Order.objects.filter(idempotency_key=idempotency_key).first()
        if existing_order:
            return existing_order

    cart_items = cart.items.all()
    if not cart_items:
        raise ValidationError("السلة فارغة")

    with transaction.atomic():
        total_amount = Decimal("0.00")
        order_items_list = []

        for item in cart_items:
            product = Product.objects.select_for_update().get(id=item.product.id)

            if not product.is_active:
                raise ValidationError(f"المنتج {product.name_ar} غير متاح")

            if product.stock < item.quantity:
                raise ValidationError(f"المخزون غير كافٍ للمنتج {product.name_ar}")

            product.stock = product.stock - item.quantity
            product.save()

            item_price = product.price * item.quantity
            total_amount = total_amount + item_price

            order_items_list.append(
                {
                    "product": product,
                    "quantity": item.quantity,
                    "price": product.price,
                }
            )

        order = Order.objects.create(
            user=user,
            total_amount=total_amount,
            idempotency_key=idempotency_key,
            status="pending",
        )

        for item_data in order_items_list:
            OrderItem.objects.create(
                order=order,
                product_id=item_data["product"].id,
                product_name_ar=item_data["product"].name_ar,
                product_name_en=item_data["product"].name_en,
                unit_price=item_data["price"],
                quantity=item_data["quantity"],
            )

        cart.items.all().delete()

        transaction.on_commit(lambda: send_order_confirmation_email.delay(order.id))

        return order


def change_order_status(order, new_status):
    allowed_transitions = {
        "pending": ["paid", "cancelled"],
        "paid": ["shipped", "cancelled"],
        "shipped": ["delivered"],
        "delivered": [],
        "cancelled": [],
    }

    current_status = order.status

    if new_status not in allowed_transitions.get(current_status, []):
        raise ValidationError(
            f"غير مسموح بالتغيير من {current_status} إلى {new_status}"
        )

    with transaction.atomic():
        if new_status == "cancelled":
            for item in order.items.all():
                product = Product.objects.select_for_update().get(id=item.product_id)
                product.stock = product.stock + item.quantity
                product.save()

        order.status = new_status
        order.save()

    return order
