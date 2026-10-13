import json
from decimal import Decimal
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from menu.models import MenuItem
from .models import Order, OrderItem
from .cart import Cart


def cart_view(request):
    cart = Cart(request)
    table_numbers = [f"Table {i}" for i in range(1, 21)]
    context = {
        'cart': cart,
        'table_numbers': table_numbers,
    }
    return render(request, 'orders/cart.html', context)


@require_POST
def add_to_cart(request):
    cart = Cart(request)
    
    # Check if JSON or form data
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
    else:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

    menu_item = get_object_or_404(MenuItem, id=item_id)
    cart.add(menu_item=menu_item, quantity=quantity)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'message': f'Added {menu_item.name} to cart',
            'cart_count': len(cart),
            'cart_subtotal': float(cart.subtotal),
            'cart_total': float(cart.grand_total),
        })

    messages.success(request, f'Added {menu_item.name} to your order.')
    return redirect('menu:index')


@require_POST
def update_cart(request):
    cart = Cart(request)
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        item_id = data.get('item_id')
        quantity = int(data.get('quantity', 1))
    else:
        item_id = request.POST.get('item_id')
        quantity = int(request.POST.get('quantity', 1))

    cart.update_quantity(item_id, quantity)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_subtotal': float(cart.subtotal),
            'tax_amount': float(cart.tax_amount),
            'cart_total': float(cart.grand_total),
        })

    return redirect('orders:cart')


@require_POST
def remove_from_cart(request):
    cart = Cart(request)
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        item_id = data.get('item_id')
    else:
        item_id = request.POST.get('item_id')

    cart.remove(item_id)

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
        return JsonResponse({
            'success': True,
            'cart_count': len(cart),
            'cart_subtotal': float(cart.subtotal),
            'tax_amount': float(cart.tax_amount),
            'cart_total': float(cart.grand_total),
        })

    messages.info(request, 'Item removed from order.')
    return redirect('orders:cart')


@require_POST
def place_order(request):
    cart = Cart(request)
    if len(cart) == 0:
        messages.error(request, 'Your cart is empty. Please add items before placing an order.')
        return redirect('menu:index')

    table_number = request.POST.get('table_number', '').strip() or 'Table 1'
    customer_name = request.POST.get('customer_name', '').strip() or 'Dine-in Guest'
    customer_notes = request.POST.get('customer_notes', '').strip()

    # Create Order
    order = Order.objects.create(
        table_number=table_number,
        customer_name=customer_name,
        customer_notes=customer_notes,
        subtotal=cart.subtotal,
        tax_amount=cart.tax_amount,
        total=cart.grand_total,
    )

    # Create OrderItems
    for item in cart:
        OrderItem.objects.create(
            order=order,
            menu_item=item['menu_item'],
            item_name=item['name'],
            unit_price=item['price'],
            quantity=item['quantity'],
            subtotal=item['subtotal'],
        )

    # Clear session cart
    cart.clear()

    messages.success(request, f'Order placed successfully! Order Code: {order.order_code}')
    return redirect('orders:track_code', order_code=order.order_code)


def track_order_view(request, order_code=None):
    code_query = request.GET.get('code', '').strip()
    active_code = order_code or code_query
    order = None

    if active_code:
        try:
            order = Order.objects.prefetch_related('items').get(order_code__iexact=active_code)
        except Order.DoesNotExist:
            order = None
            if active_code:
                messages.error(request, f'No active order found with code "{active_code}". Please verify.')

    context = {
        'order': order,
        'search_code': active_code or '',
    }
    return render(request, 'orders/track.html', context)


def order_status_api(request, order_code):
    order = get_object_or_404(Order, order_code__iexact=order_code)
    
    # Progress step index (0 to 3)
    status_steps = {
        Order.Status.PENDING: 1,
        Order.Status.PREPARING: 2,
        Order.Status.READY: 3,
        Order.Status.SERVED: 4,
        Order.Status.CANCELLED: -1,
    }
    
    return JsonResponse({
        'order_code': order.order_code,
        'table_number': order.table_number,
        'status': order.status,
        'status_display': order.get_status_display(),
        'step_number': status_steps.get(order.status, 1),
        'created_at': order.created_at.strftime('%I:%M %p'),
        'total': float(order.total),
        'item_count': sum(i.quantity for i in order.items.all()),
    })
