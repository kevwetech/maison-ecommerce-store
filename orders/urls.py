from django.urls import path
from . import views

urlpatterns = [
    path('cart/', views.cart_page, name='cart_page'),
    path('cart/add/<int:product_id>/', views.cart_add, name='cart_add'),
    path('cart/remove/<int:product_id>/', views.cart_remove, name='cart_remove'),
    path('cart/decrease/<int:product_id>/', views.cart_decrease, name='cart_decrease'),
    path('checkout/', views.checkout, name='checkout'),
    path('my-orders/', views.order_list, name='order_list'),
    path('order/<int:order_id>/', views.order_detail, name='order_detail'),
    path('payment/verify/<int:order_id>/', views.payment_verify, name='payment_verify'),
    path('track/', views.track_order, name='track_order'),
]