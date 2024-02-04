from . import views
from django.urls import path
from rest_framework_nested import routers

router = routers.DefaultRouter()
router.register('resipis', views.ResipiViewSet, basename='resipis')
router.register('categories', views.CategoryViewSet, basename='categories')
#router.register('categories/<slug:slug>', views.CategoryResipiViewSet, basename='categories')
router.register('chefs', views.ChefViewSet, basename='chefs')
#router.register('carts', views.CartViewSet)
#router.register('customers', views.Chef)

resipis_router = routers.NestedDefaultRouter(router, 'resipis', lookup='resipi_pk')
chefs_router = routers.NestedDefaultRouter(router, 'chefs', lookup='chef_pk')
#categories_router = routers.NestedDefaultRouter(router, 'categories', lookup='category_pk')
#resipis_router.register('reviews', views.ReviewViewSet, basename='product-reviews')
#resipis_router.register('images', views.ProductImageViewSet, basename='product-images')

urlpatterns = [
    path('categories/<slug:slug>/', views.CategoryResipiViewSet.as_view(), name='category-resipis'),
]

allelse = router.urls + resipis_router.urls + chefs_router.urls 
# + categories_router.urls


urlpatterns += allelse