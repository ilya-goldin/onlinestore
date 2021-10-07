from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter, ReviewFilter, OrderFilter
from .models import Product, Review, Order, Collection
from .premissions import IsCreator, IsOrderCreator
from .serializers import ProductSerializer, ReviewSerializer, OrderSerializer, CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ReviewFilter

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsCreator()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        return []


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = OrderFilter

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            return [IsOrderCreator()]
        elif self.action in ['create']:
            return [IsAuthenticated()]
        elif self.action in ['destroy']:
            return[IsAdminUser()]
        return []

    def get_queryset(self):
        req_qp = self.request.query_params
        product = req_qp.get('product')
        product = product.split(',') if product else product
        params = {
            'status': req_qp.get('status'),
            'created_at__gte': req_qp.get('created_at_after'),
            'created_at__lte': req_qp.get('created_at_before'),
            'updated_at__gte': req_qp.get('updated_at_after'),
            'updated_at__lte': req_qp.get('updated_at_before'),
            'products__in': product,
            'order_value__lte': req_qp.get('order_value_max'),
            'order_value__gte': req_qp.get('order_value_min'),
        }
        query_params = {k: v for k, v in params.items() if v is not None and v != ''}
        if self.request.user.is_staff:
            queryset = Order.objects.filter(**query_params)
        else:
            queryset = Order.objects.filter(
                user=self.request.user,
                **query_params
            )
        return queryset


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [IsAdminUser()]
        return []
