from django.contrib import admin
from django.db.models.signals import post_save, pre_delete
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


def calculate_total_add(sender, instance, **kwargs):
    price = instance.product.price
    qty = instance.qty
    order = instance.order
    order.order_value += (price * qty)
    order.save()


def calculate_total_remove(sender, instance, **kwargs):
    price = instance.product.price
    qty = instance.qty
    order = instance.order
    order.order_value -= (price * qty)
    order.save()


post_save.connect(calculate_total_add, sender=OrderProducts)
pre_delete.connect(calculate_total_remove, sender=OrderProducts)
