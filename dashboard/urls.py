from django.urls import path
from . import views

urlpatterns = [
    path('', views.dashboard_home, name='dashboard_home'),
    path('products/', views.product_list, name='dashboard_products'),
    path('products/add/', views.product_add, name='dashboard_product_add'),
    path('products/edit/<int:product_id>/', views.product_edit, name='dashboard_product_edit'),
    path('orders/', views.order_list, name='dashboard_orders'),
    path('orders/<int:order_id>/', views.order_detail, name='dashboard_order_detail'),
    path('categories/', views.category_list, name='dashboard_categories'),
    path('categories/add/', views.category_add, name='dashboard_category_add'),
    path('categories/edit/<int:category_id>/', views.category_edit, name='dashboard_category_edit'),
    path('categories/delete/<int:category_id>/', views.category_delete, name='dashboard_category_delete'),
    path('orders/<int:order_id>/status/', views.order_update_status, name='dashboard_order_status'),
    path('products/image/delete/<int:image_id>/', views.delete_product_image, name='delete_product_image'),
    path('delivery-options/', views.delivery_options, name='dashboard_delivery_options'),
    path('delivery-options/add/', views.delivery_option_add, name='dashboard_delivery_option_add'),
    path('delivery-options/edit/<int:option_id>/', views.delivery_option_edit, name='dashboard_delivery_option_edit'),
    path('delivery-options/delete/<int:option_id>/', views.delivery_option_delete, name='dashboard_delivery_option_delete'),
]