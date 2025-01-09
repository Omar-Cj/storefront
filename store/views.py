from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, OrderItem, Product, Collection, Review
from .serializers import CartItemSerializer, CartSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['unit_price']
    pagination_class = DefaultPagination
    search_fields = ['title']
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Cannot Delete product because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 
        return super().destroy(request, *args, **kwargs)


    


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).order_by('id')
    serializer_class = CollectionSerializer

    def destroy(self, request, *args, **kwargs):
        if Product.objects.filter(collection_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Cannot delete collection because it has products'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
        return super().destroy(request, *args, **kwargs)

   
class ReviewViewSet(ModelViewSet):
    serializer_class =  ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk'])
    
    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
    

class CartViewSet(CreateModelMixin,RetrieveModelMixin,DestroyModelMixin,GenericViewSet):
    queryset = Cart.objects.prefetch_related('items__product').all()
    serializer_class = CartSerializer


class CartItemViewSet(ModelViewSet):
    serializer_class = CartItemSerializer

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])

    

