from django.urls import path

from .import views

app_name = 'client'

urlpatterns = [
    path('', views.client, name='client'),
    path('<int:telegram_id>/', views.client_detail, name='client_detail'),
    path('order-times/<int:order_id>/', views.order_times, name='order_times'),
    path('order-check/<int:order_id>/', views.order_check, name='order_check'),
]

