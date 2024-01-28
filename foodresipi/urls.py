from . import views
from django.urls import path
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('resipis', views.ResipiViewSet, basename='resipis')
router.register('categories', views.CategoryViewSet)
#router.register('carts', views.CartViewSet)
#router.register('customers', views.Chef)

resipis_router = routers.NestedDefaultRouter(router, 'resipis', lookup='resipi_pk')
#resipis_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
#resipis_router.register('images', views.ProductImageViewSet, basename='product-images')

urlpatterns = router.urls + resipis_router.urls

