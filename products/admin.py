from django.contrib import admin
from .models import Product, Collection, Review, Order, OrderProducts


class ReviewsInLine(admin.TabularInline):
    model = Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewsInLine]
    list_display = ('name', 'price', 'created_at')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at')


class ProductInLine(admin.TabularInline):
    model = OrderProducts


@admin.display(description='Products')
def total_products(obj):
    return obj.orderproducts_set.count()


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInLine]
    list_display = ('user', 'status', 'order_value', total_products, 'created_at', 'updated_at')
    ordering = '-created_at',


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'score', 'created_at')
