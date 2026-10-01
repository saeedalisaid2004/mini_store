from cart.models import Cart


def get_user_cart(*, user) -> Cart:
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart
