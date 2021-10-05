from rest_framework.routers import DefaultRouter
from .api_views import ProductViewSet, ReviewViewSet, OrderViewSet, CollectionViewSet

router = DefaultRouter()
router.register('products', ProductViewSet)
router.register('product-reviews', ReviewViewSet)
router.register('orders', OrderViewSet)
router.register('product-collections', CollectionViewSet)

urlpatterns = router.urls
