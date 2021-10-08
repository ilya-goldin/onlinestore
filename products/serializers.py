from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.serializers import ModelSerializer,\
    PrimaryKeyRelatedField, ValidationError, CharField
from .models import Product, Review, Order, OrderProducts, Collection


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
        user = User.objects.get(id=self.context['request'].user.id)
        reviews = user.reviews.filter(product_id=validated_data.get('product').id)
        if list(reviews):
            raise ValidationError('You can leave only one review for each product ')
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)


class OrderProductSerializer(ModelSerializer):
    """Serializer for the OrderProduct"""

    class Meta:
        model = OrderProducts
        fields = 'id', 'product', 'qty'


class OrderSerializer(ModelSerializer):
    """Serializer for the Order"""

    product = OrderProductSerializer(source='orderproducts_set', many=True)

    class Meta:
        model = Order
        read_only_fields = 'create_date', 'update_date'
        fields = 'status', 'order_value', 'created_at', 'updated_at', 'product'

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        validated_data['order_value'] = 0
        products = validated_data.pop('orderproducts_set')
        for prod in products:
            validated_data['order_value'] += prod['product'].price * prod['qty']
        order = Order.objects.create(**validated_data)
        orderproducts = [OrderProducts(order=order, **product) for product in products]
        OrderProducts.objects.bulk_create(orderproducts)
        return order

    def update(self, instance, validated_data):
        products = validated_data.pop('orderproducts_set')
        order_value = 0
        for prod in products:
            order_value += prod['product'].price * prod['qty']
        instance.order_value = order_value
        if 'status' in validated_data:
            if self.context['request'].user.is_staff:
                instance.status = validated_data.pop('status')
            else:
                raise ValidationError('You can`n change order status!')
        instance.save()
        orderproducts = [OrderProducts(order=instance, **product) for product in products]
        OrderProducts.objects.bulk_create(orderproducts)
        return instance


class CollectionSerializer(ModelSerializer):
    """Serializer for the Collection"""

    class Meta:
        model = Collection
        fields = 'title', 'note', 'items', 'created_at', 'updated_at'


class TokenSerializer(ModelSerializer):
    username = UserSerializer(
        read_only=True,
    )
    password = CharField()

    class Meta:
        model = Token
        fields = 'username', 'password'
