from decimal import Decimal

import django.test
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError

from cart.services import add_or_update_cart_item
from catalog.models import Category, Product


class Week1Tests(django.test.TestCase):
    def test_create_product_and_cart(self):
        user = User.objects.create_user(username="testuser", password="password123")
        category = Category.objects.create(
            name_ar="إلكترونيات", name_en="Electronics", slug="electronics"
        )
        product = Product.objects.create(
            category=category,
            name_ar="هاتف",
            name_en="Phone",
            slug="phone",
            price=Decimal("1500.00"),
            stock=10,
            is_active=True,
        )

        cart_item = add_or_update_cart_item(
            user=user, product_id=product.id, quantity=2
        )
        self.assertEqual(cart_item.quantity, 2)
        self.assertEqual(cart_item.cart.user, user)

    def test_add_to_cart_exceeds_stock(self):
        user = User.objects.create_user(username="testuser2", password="password123")
        category = Category.objects.create(
            name_ar="أجهزة", name_en="Devices", slug="devices"
        )
        product = Product.objects.create(
            category=category,
            name_ar="حاسوب",
            name_en="Laptop",
            slug="laptop",
            price=Decimal("3000.00"),
            stock=3,
            is_active=True,
        )

        with self.assertRaises(ValidationError):
            add_or_update_cart_item(user=user, product_id=product.id, quantity=5)
