from decimal import Decimal
from menu.models import MenuItem


CART_SESSION_ID = 'rasoi_cart'
TAX_RATE = Decimal('0.03')  # 3% tax as per Rasoi restaurant footer


class Cart:
    def __init__(self, request):
        self.session = request.session
        cart = self.session.get(CART_SESSION_ID)
        if not cart:
            cart = self.session[CART_SESSION_ID] = {}
        self.cart = cart

    def add(self, menu_item, quantity=1, override_quantity=False):
        item_id = str(menu_item.id)
        if item_id not in self.cart:
            self.cart[item_id] = {
                'id': menu_item.id,
                'name': menu_item.name,
                'price': str(menu_item.price),
                'quantity': 0,
                'image_url': menu_item.image_url or '',
                'is_veg': menu_item.is_veg,
            }
        if override_quantity:
            self.cart[item_id]['quantity'] = quantity
        else:
            self.cart[item_id]['quantity'] += quantity

        if self.cart[item_id]['quantity'] <= 0:
            self.remove(menu_item)
        else:
            self.save()

    def remove(self, menu_item):
        item_id = str(menu_item.id) if hasattr(menu_item, 'id') else str(menu_item)
        if item_id in self.cart:
            del self.cart[item_id]
            self.save()

    def update_quantity(self, item_id, quantity):
        item_id = str(item_id)
        if item_id in self.cart:
            if quantity <= 0:
                self.remove(item_id)
            else:
                self.cart[item_id]['quantity'] = quantity
                self.save()

    def clear(self):
        self.session[CART_SESSION_ID] = {}
        self.save()

    def save(self):
        self.session.modified = True

    def __iter__(self):
        item_ids = self.cart.keys()
        menu_items = MenuItem.objects.filter(id__in=item_ids)
        items_map = {str(item.id): item for item in menu_items}

        for item_id, item_data in self.cart.items():
            price = Decimal(item_data['price'])
            qty = item_data['quantity']
            subtotal = price * qty
            yield {
                'id': item_id,
                'menu_item': items_map.get(item_id),
                'name': item_data['name'],
                'price': price,
                'quantity': qty,
                'subtotal': subtotal,
                'image_url': item_data.get('image_url', ''),
                'is_veg': item_data.get('is_veg', True),
            }

    def __len__(self):
        return sum(item['quantity'] for item in self.cart.values())

    @property
    def total_count(self):
        return len(self)

    @property
    def subtotal(self):
        return sum(Decimal(item['price']) * item['quantity'] for item in self.cart.values())

    @property
    def tax_amount(self):
        return round(self.subtotal * TAX_RATE, 2)

    @property
    def grand_total(self):
        return self.subtotal + self.tax_amount
