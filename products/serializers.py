from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, PrimaryKeyRelatedField
from .models import Product, Review, Order, Collection


class UserSerializer(ModelSerializer):
    """Serializer for the User."""

    class Meta:
        model = User
        fields = 'id', 'username', 'first_name', 'last_name'


class ProductSerializer(ModelSerializer):
    """Serializer for the Product"""

    class Meta:
        model = Product
        fields = 'name', 'description', 'price', 'created_at', 'updated_at'


class ReviewSerializer(ModelSerializer):
    """Serializer for the Review"""

    user = UserSerializer(
        read_only=True,
    )
    product_id = PrimaryKeyRelatedField(
        source='product',
        queryset=Product.objects.all(),
    )

    class Meta:
        model = Review
        fields = 'user', 'review_text', 'product_id', 'score', 'created_at', 'updated_at'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderSerializer(ModelSerializer):
    """Serializer for the Order"""

    user = UserSerializer(
        read_only=True,
    )

    class Meta:
        model = Order
        fields = 'user', 'status', 'order_value', 'created_at', 'updated_at', 'items'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class CollectionSerializer(ModelSerializer):
    class Meta:
        model = Collection
        fields = 'title', 'note', 'items', 'created_at', 'updated_at'
