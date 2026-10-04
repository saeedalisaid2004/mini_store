from cart.models import Cart


def get_user_cart(*, user):
    """
    Selector should only fetch the cart if it exists.
    Creating a cart is a mutation and belongs to services.py.
    """
    return Cart.objects.filter(user=user).prefetch_related("items__product").first()
