from orders.models import Order


def get_user_orders(user):

    return Order.objects.filter(user=user)


def get_user_order_detail(user, order_id):

    try:
        return Order.objects.get(id=order_id, user=user)
    except Order.DoesNotExist:
        return None
