from django.urls import path

from .import views

urlpatterns = [
    path('client/<int:client_id>/', views.client_detail, name='client_detail'),
    path('register/', views.register_client, name='register_client'),
    path('receive-code/<int:client_id>/', views.receive_code, name='receive_code'),
    path('products-list/', views.products_list, name='products_list'),
    path('order-product/<int:product_id>/', views.order_product, name='order_product'),
]

