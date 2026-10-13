from django.test import TestCase, Client
from django.urls import reverse
from decimal import Decimal
from menu.models import Category, MenuItem
from orders.models import Order


class MenuAndOrderingTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name='Mains', slug='mains')
        self.item = MenuItem.objects.create(
            category=self.category,
            name='Butter Chicken',
            slug='butter-chicken',
            description='Creamy tomato gravy with charred chicken',
            price=Decimal('420.00'),
            is_veg=False
        )

    def test_menu_page_loads(self):
        response = self.client.get(reverse('menu:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Butter Chicken')

    def test_cart_add_and_checkout(self):
        # Add item to cart
        add_response = self.client.post(
            reverse('orders:add_to_cart'),
            {'item_id': self.item.id, 'quantity': 2}
        )
        self.assertEqual(add_response.status_code, 302)

        # Checkout
        checkout_response = self.client.post(
            reverse('orders:checkout'),
            {'table_number': 'Table 5', 'customer_name': 'Test Guest', 'customer_notes': 'Extra napkin'}
        )
        self.assertEqual(checkout_response.status_code, 302)

        # Check Order in DB
        order = Order.objects.first()
        self.assertIsNotNone(order)
        self.assertEqual(order.table_number, 'Table 5')
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.items.first().quantity, 2)
        # 420 * 2 = 840; tax 3% = 25.20; total = 865.20
        self.assertEqual(order.subtotal, Decimal('840.00'))
        self.assertEqual(order.tax_amount, Decimal('25.20'))
        self.assertEqual(order.total, Decimal('865.20'))
