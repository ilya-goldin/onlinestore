from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter
from .models import Product, Review, Order, Collection
from .premissions import IsCreator
from .serializers import ProductSerializer, ReviewSerializer, OrderSerializer, CollectionSerializer


class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = ProductFilter

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", 'destroy']:
            return [IsAdminUser()]
        return []


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.all()
    serializer_class = ReviewSerializer
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", 'destroy']:
            return [IsAdminUser(), IsCreator()]
        return []


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", 'destroy']:
            return [IsAdminUser(), IsAuthenticated()]
        elif self.action in ['get']:
            return [IsCreator(), IsAdminUser()]
        return []


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.all()
    serializer_class = CollectionSerializer
    filter_backends = [DjangoFilterBackend]

    def get_permissions(self):
        if self.action in ["create", "update", "partial_update", 'destroy']:
            return [IsAdminUser()]
        return []
