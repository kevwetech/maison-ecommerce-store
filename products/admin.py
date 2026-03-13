from django.contrib import admin
from .models import Product, Category, ProductImage, Review, Wishlist

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]

admin.site.register(Category)
admin.site.register(Wishlist)
admin.site.register(Review)