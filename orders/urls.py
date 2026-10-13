from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('cart/', views.cart_view, name='cart'),
    path('cart/add/', views.add_to_cart, name='add_to_cart'),
    path('cart/update/', views.update_cart, name='update_cart'),
    path('cart/remove/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.place_order, name='checkout'),
    path('track/', views.track_order_view, name='track'),
    path('track/<str:order_code>/', views.track_order_view, name='track_code'),
    path('api/status/<str:order_code>/', views.order_status_api, name='order_status_api'),
]
