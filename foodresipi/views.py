from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
#from store.permissions import IsAdminOrReadOnly, ViewCustomerHistoryPermission
from .filters import ResipiFilter
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from rest_framework import status
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics
from rest_framework.mixins import UpdateModelMixin, CreateModelMixin, DestroyModelMixin, RetrieveModelMixin
from .serializers import CategorySerializer, ResipiImageSerializer, ResipiSerializer, ReviewSerializer, ChefSerializer, CategoryResipiSerializer
from .models import Resipi, Category, Chef, ResipiImage, ResipiRating, Review
#from store.pagination import DefaultPagination
from django.db.models.aggregates import Count, Avg


class ResipiViewSet(ModelViewSet):
    queryset = Resipi.objects.prefetch_related('images').all()
    serializer_class = ResipiSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ResipiFilter
    #pagination_class = DefaultPagination
    #permission_classes = [IsAdminOrReadOnly]
    search_fields = ['title', 'description']
    ordering_fields = ['title', 'last_update']


    def destroy(self, request, *args, **kwargs):
        if Category.objects.filter(resipi_id=kwargs['pk']).count > 0:
            return Response({'error': 'cant delete'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CategoryViewSet(ModelViewSet):
    queryset = Category.objects.annotate(resipis_count=Count('resipis'))
    serializer_class = CategorySerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['id', 'title', 'resipis_count']

    # def retrieve(self, request, *args, **kwargs):
    #     if Resipi.objects.filter(category_id=kwargs['pk']):
    #         queryset = Resipi.objects.filter(category_id=kwargs['pk']).all()
    #         return Response(status=status.HTTP_200_OK, data=queryset)

    def destroy(self, request, *args, **kwargs):
        if Resipi.objects.filter(category_id=kwargs['pk']):
            return Response({'error': 'cant delete'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

class CategoryResipiViewSet(generics.ListAPIView):
    def get_queryset(self):
        print(self.kwargs)
        return Resipi.objects.filter(category__slug=self.kwargs['slug'])
    lookup_field = ['slug']
    serializer_class = CategoryResipiSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['title']
    ordering_fields = ['id', 'title', 'resipis_count']

    def get_serializer_context(self):
        return {'category__slug': self.kwargs['slug']}


class ChefViewSet(generics.RetrieveAPIView, generics.ListAPIView, GenericViewSet):
    # def get_queryset(self):
    #     return Chef.objects.filter(id=self.kwargs['pk'])
    queryset = Chef.objects.all()

    serializer_class = ChefSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    search_fields = ['user_id']


class ReviewViewSet(ModelViewSet):    
    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk_pk'])

    def get_serializer_context(self):
        context = super(ReviewViewSet, self).get_serializer_context()
        context.update({'product_id': self.kwargs['product_pk_pk']})
        return context