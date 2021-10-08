from django.contrib.auth.hashers import check_password
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from rest_framework.exceptions import ValidationError
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from .filters import ProductFilter, ReviewFilter, OrderFilter
from .models import Product, Review, Order, Collection
from .premissions import IsCreator, IsOrderCreator
from .serializers import ProductSerializer, ReviewSerializer,\
    OrderSerializer, CollectionSerializer, TokenSerializer
from rest_framework.authtoken.models import Token


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


class TokenViewSet(ModelViewSet):
    queryset = Token.objects.all()
    serializer_class = TokenSerializer

    def get_permissions(self):
        if self.action == 'list':
            return [IsAuthenticated()]
        return [IsAdminUser()]

    def get_queryset(self):
        username = self.request.query_params.get('username')
        password = self.request.query_params.get('password')
        try:
            user = User.objects.get(username=username)
        except BaseException as e:
            raise ValidationError({"400": f'{str(e)}'})
        if not check_password(password, user.password):
            raise ValidationError({"message": "Incorrect Login credentials"})

        token = Token.objects.get_or_create(user=user)[0].key
        if user and user.is_active:
            resp = {"token": token}
            return Response(resp)
        else:
            raise ValidationError({"400": f'Account not active or doesnt exist'})
