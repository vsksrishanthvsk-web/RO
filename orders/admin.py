from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('subtotal',)


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_code', 'table_number', 'customer_name', 'status', 'total', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('order_code', 'table_number', 'customer_name')
    readonly_fields = ('order_code', 'subtotal', 'tax_amount', 'total', 'created_at', 'updated_at')
    inlines = [OrderItemInline]
