from django.urls import path
from . import views

app_name = 'kitchen'

urlpatterns = [
    path('', views.kitchen_display_view, name='display'),
    path('update/<str:order_code>/', views.update_order_status, name='update_status'),
    path('api/orders/', views.kitchen_orders_api, name='orders_api'),
]
