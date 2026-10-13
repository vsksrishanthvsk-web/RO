import random
import string
from django.db import models
from menu.models import MenuItem


def generate_order_code():
    chars = string.ascii_uppercase + string.digits
    suffix = ''.join(random.choices(chars, k=5))
    return f"RSO-{suffix}"


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Order Received'
        PREPARING = 'PREPARING', 'In the Kitchen'
        READY = 'READY', 'Ready to Serve'
        SERVED = 'SERVED', 'Served'
        CANCELLED = 'CANCELLED', 'Cancelled'

    order_code = models.CharField(max_length=20, unique=True, default=generate_order_code)
    table_number = models.CharField(max_length=20, help_text="e.g. Table 4")
    customer_name = models.CharField(max_length=100, blank=True, default='Guest')
    customer_notes = models.TextField(blank=True, default='', help_text="Any allergy or special preparation requests")
    
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
        db_index=True
    )
    
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    tax_rate = models.DecimalField(max_digits=4, decimal_places=2, default=0.03, help_text="3% tax")
    tax_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.order_code} - {self.table_number} ({self.get_status_display()})"

    def recalculate_totals(self):
        items = self.items.all()
        sub = sum(item.subtotal for item in items)
        self.subtotal = sub
        self.tax_amount = round(sub * self.tax_rate, 2)
        self.total = self.subtotal + self.tax_amount
        self.save(update_fields=['subtotal', 'tax_amount', 'total'])


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    menu_item = models.ForeignKey(MenuItem, on_delete=models.SET_NULL, null=True, blank=True)
    item_name = models.CharField(max_length=200)
    unit_price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.subtotal = self.unit_price * self.quantity
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.quantity}x {self.item_name} for {self.order.order_code}"
