from decimal import Decimal

from django.core.exceptions import ValidationError
from django.db import transaction

from catalog.models import Product
from orders.models import Order, OrderItem
from orders.tasks import send_order_confirmation_email


def checkout_cart(user, cart, idempotency_key=None):
    # 1. Scope Idempotency check to the CURRENT USER first
    if idempotency_key:
        existing_order = Order.objects.filter(
            user=user, idempotency_key=idempotency_key
        ).first()
        if existing_order:
            return existing_order

    # 2. Everything inside a single atomic transaction
    with transaction.atomic():
        # Lock cart to prevent concurrent checkouts on the same cart
        cart_items = (
            cart.items.select_related("product")
            .select_for_update()
            .order_by("product_id")
        )

        if not cart_items.exists():
            raise ValidationError("السلة فارغة")

        total_amount = Decimal("0.00")
        order_items_list = []

        # Lock products in deterministic order (by ID) to avoid deadlocks
        for item in cart_items:
            try:
                product = Product.objects.select_for_update().get(id=item.product.id)
            except Product.DoesNotExist:
                raise ValidationError(f"المنتج {item.product.name_ar} غير موجود")

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

        # Create Order with user relation & idempotency key
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

        # Clear cart items safely
        cart.items.all().delete()

        # Queue confirmation email on successful commit
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

    with transaction.atomic():
        # Lock the order row first to prevent race conditions on status updates
        locked_order = Order.objects.select_for_update().get(id=order.id)
        current_status = locked_order.status

        if new_status not in allowed_transitions.get(current_status, []):
            raise ValidationError(
                f"غير مسموح بالتغيير من {current_status} إلى {new_status}"
            )

        # Safely restore stock if cancelling
        if new_status == "cancelled":
            for item in locked_order.items.all():
                try:
                    product = Product.objects.select_for_update().get(
                        id=item.product_id
                    )
                    product.stock = product.stock + item.quantity
                    product.save()
                except Product.DoesNotExist:
                    # Ignore stock restoration if product was deleted
                    pass

        locked_order.status = new_status
        locked_order.save()

        return locked_order
