from django.urls import path
from . import views

urlpatterns = [
    path('', views.products_page, name='products_page'),
    path('product/<int:product_id>/', views.product_details, name='product_details'),
    path('create/', views.product_create, name='product_create'),
    path('<int:pk>/update/', views.product_update, name='product_update'),
    path('<int:pk>/delete/', views.product_delete, name='product_delete'),
    path('categories/', views.categories_page, name='categories_page'),
    path('wishlist/', views.wishlist_page, name='wishlist_page'),
    path('wishlist/toggle/<int:product_id>/', views.toggle_wishlist, name='toggle_wishlist'),
    path('review/<int:product_id>/', views.add_review, name='add_review'),
    path('about/', views.about_page, name='about_page'),
    path('contact/', views.contact_page, name='contact_page'),
]
