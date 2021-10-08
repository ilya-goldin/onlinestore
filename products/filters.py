from django_filters import rest_framework as filters
from .models import Product, Review, Order, OrderStatusChoices


class ProductFilter(filters.FilterSet):
    price = filters.RangeFilter()

    class Meta:
        model = Product
        fields = {
            'name': ['contains'],
            'description': ['contains']
        }


class ReviewFilter(filters.FilterSet):
    product = filters.ModelChoiceFilter(
        field_name='product',
        to_field_name='id',
        queryset=Product.objects.all(),
    )
    created_at = filters.DateTimeFromToRangeFilter()

    class Meta:
        model = Review
        fields = ['user', 'product', 'created_at']


class OrderFilter(filters.FilterSet):
    status = filters.ChoiceFilter(
        choices=OrderStatusChoices.choices
    )
    order_value = filters.RangeFilter()
    created_at = filters.DateFromToRangeFilter()
    updated_at = filters.DateFromToRangeFilter()

    class Meta:
        model = Order
        fields = ['status', 'order_value', 'products', 'created_at', 'updated_at']
