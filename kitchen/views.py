import json
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
from orders.models import Order


def kitchen_display_view(request):
    active_statuses = [Order.Status.PENDING, Order.Status.PREPARING, Order.Status.READY]
    active_orders = Order.objects.filter(status__in=active_statuses).prefetch_related('items').order_by('created_at')
    
    recent_served = Order.objects.filter(status=Order.Status.SERVED).prefetch_related('items').order_by('-updated_at')[:8]

    pending_count = active_orders.filter(status=Order.Status.PENDING).count()
    preparing_count = active_orders.filter(status=Order.Status.PREPARING).count()
    ready_count = active_orders.filter(status=Order.Status.READY).count()

    context = {
        'active_orders': active_orders,
        'recent_served': recent_served,
        'pending_count': pending_count,
        'preparing_count': preparing_count,
        'ready_count': ready_count,
        'total_active': active_orders.count(),
    }
    return render(request, 'kitchen/display.html', context)


@require_POST
def update_order_status(request, order_code):
    order = get_object_or_404(Order, order_code__iexact=order_code)
    
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        new_status = data.get('status')
    else:
        new_status = request.POST.get('status')

    valid_statuses = [s.value for s in Order.Status]
    if new_status in valid_statuses:
        order.status = new_status
        order.save(update_fields=['status', 'updated_at'])
        
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({
                'success': True,
                'order_code': order.order_code,
                'status': order.status,
                'status_display': order.get_status_display(),
            })
        messages.success(request, f"Order {order.order_code} updated to {order.get_status_display()}")
    else:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.content_type == 'application/json':
            return JsonResponse({'success': False, 'error': 'Invalid status'}, status=400)
        messages.error(request, "Invalid status update requested.")

    return redirect('kitchen:display')


def kitchen_orders_api(request):
    active_statuses = [Order.Status.PENDING, Order.Status.PREPARING, Order.Status.READY]
    active_orders = Order.objects.filter(status__in=active_statuses).prefetch_related('items').order_by('created_at')

    data = []
    for order in active_orders:
        items = [{'name': item.item_name, 'quantity': item.quantity} for item in order.items.all()]
        data.append({
            'order_code': order.order_code,
            'table_number': order.table_number,
            'customer_name': order.customer_name,
            'customer_notes': order.customer_notes,
            'status': order.status,
            'status_display': order.get_status_display(),
            'created_at': order.created_at.strftime('%I:%M %p'),
            'items': items,
        })

    return JsonResponse({'orders': data, 'count': len(data)})
