from django.urls import path
from . import views

app_name = 'menu'

urlpatterns = [
    path('', views.menu_view, name='index'),
    path('api/dish/<int:item_id>/', views.dish_detail_api, name='dish_detail_api'),
]
