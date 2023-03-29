from django.urls import path
from django.contrib.auth.views import LogoutView
from .import views

app_name = 'dashboard'

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('', views.dashboard, name='dashboard'),
    # category
    path('category/', views.category, name='category'),
    path('category-form/', views.category_form, name='category_form'),
    path('category-form/<int:category_id>/', views.category_update_form, name='category_update_form'),
    path('category-delete/<int:category_id>/', views.category_delete_form, name='category_delete_form'),
    # product
    path('product/', views.product, name='product'),
    path('product-form/', views.product_form, name='product_form'),
    path('product-form/<int:product_id>/', views.product_update_form, name='product_update_form'),
    path('product-delete/<int:product_id>/', views.product_delete_form, name='product_delete_form'),
    # promo
    path('promo/', views.promo, name='promo'),
    path('promo-form/', views.promo_form, name='promo_form'),
    path('promo-delete/<int:promo_id>/', views.promo_delete_form, name='promo_delete_form'),
    path('promo-delete-date/', views.promo_delete_date, name='promo_delete_date'),
    path('promo-print/', views.promo_print, name='promo_print'),
]


