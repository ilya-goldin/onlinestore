from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, ReviewViewSet, OrderViewSet, CollectionViewSet

router = DefaultRouter()
router.register('products', ProductViewSet, basename='products')
router.register('product-reviews', ReviewViewSet, basename='product-reviews')
router.register('orders', OrderViewSet, basename='orders')
router.register('product-collections', CollectionViewSet, basename='product-collections')

urlpatterns = router.urls
