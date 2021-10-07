from django.contrib import admin
from .models import Product, Collection, Review, Order, OrderProducts


class ReviewsInLine(admin.TabularInline):
    model = Review


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ReviewsInLine]
    list_display = ('id', 'name', 'price')


@admin.register(Collection)
class CollectionAdmin(admin.ModelAdmin):
    list_display = ('title',)


class ProductInLine(admin.TabularInline):
    model = OrderProducts


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    inlines = [ProductInLine]
    list_display = ('user', 'status', 'order_value', 'created_at', 'updated_at')

