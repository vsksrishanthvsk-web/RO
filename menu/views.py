from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.db.models import Q
from .models import Category, MenuItem


def menu_view(request):
    categories = Category.objects.all()
    items = MenuItem.objects.filter(is_available=True)

    category_slug = request.GET.get('category', '').strip()
    search_query = request.GET.get('q', '').strip()
    veg_only = request.GET.get('veg', '').strip()

    active_category = None
    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug)
        items = items.filter(category=active_category)

    if search_query:
        items = items.filter(
            Q(name__icontains=search_query) |
            Q(description__icontains=search_query)
        )

    if veg_only == '1':
        items = items.filter(is_veg=True)

    context = {
        'categories': categories,
        'items': items,
        'active_category': active_category,
        'search_query': search_query,
        'veg_only': veg_only,
    }
    return render(request, 'menu/index.html', context)


def dish_detail_api(request, item_id):
    item = get_object_or_404(MenuItem, id=item_id)
    return JsonResponse({
        'id': item.id,
        'name': item.name,
        'category': item.category.name,
        'description': item.description,
        'price': float(item.price),
        'image_url': item.image_url,
        'is_veg': item.is_veg,
        'is_spicy': item.is_spicy,
        'prep_time_minutes': item.prep_time_minutes,
    })
