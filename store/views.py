from django.db.models.aggregates import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.mixins import CreateModelMixin,RetrieveModelMixin, DestroyModelMixin, UpdateModelMixin
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework import status

from .permissions import FullDjangoModelPermissions, IsAdminUserOrReadOnly, ViewCustomerHistoryPermission
from .pagination import DefaultPagination
from .filters import ProductFilter
from .models import Cart, CartItem, Customer, Order, OrderItem, Product, Collection, Review
from .serializers import AddCartItemSerializer, CartItemSerializer, CartSerializer, CreateOrderSerializer, CustomerSerializer, OrderSerializer, ProductSerializer, CollectionSerializer, ReviewSerializer, UpdateCartItemSerializer, UpdateOrderSerializer



class ProductViewSet(ModelViewSet):
    queryset = Product.objects.all().order_by('id')
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_class = ProductFilter
    ordering_fields = ['unit_price']
    pagination_class = DefaultPagination
    permission_classes = [IsAdminUserOrReadOnly]
    search_fields = ['title']
    serializer_class = ProductSerializer

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['pk']).count() > 0:
            return Response({'error': 'Cannot Delete product because it is associated with an order item'}, status=status.HTTP_405_METHOD_NOT_ALLOWED) 
        return super().destroy(request, *args, **kwargs)


    


class CollectionViewSet(ModelViewSet):
    queryset = Collection.objects.annotate(products_count=Count('products')).order_by('id')
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminUserOrReadOnly]

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
    http_method_names = ['get', 'post', 'patch', 'delete']

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return AddCartItemSerializer
        elif self.request.method == 'PATCH':
            return UpdateCartItemSerializer
        return CartItemSerializer
    
    def get_serializer_context(self):
        return {'cart_id': self.kwargs['cart_pk']}

    def get_queryset(self):
        return CartItem.objects.select_related('product').filter(cart_id=self.kwargs['cart_pk'])

    

class CustomerViewset(ModelViewSet):
    queryset = Customer.objects.all()
    serializer_class = CustomerSerializer
    permission_classes = [IsAdminUser]

    @action(detail=True, permission_classes=[ViewCustomerHistoryPermission] )
    def history(self, request, pk):
        return Response('ok')

    @action(detail=False, methods=['GET', 'PUT'], permission_classes=[IsAuthenticated])
    def me(self, request):
        customer = Customer.objects.get(user_id=request.user.id)
        if request.method == 'GET':
            serializer = CustomerSerializer(customer)
            return Response(serializer.data)
        elif request.method == 'PUT':
            serializer = CustomerSerializer(customer, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data)
        


class OrderViewset(ModelViewSet):
    http_method_names = ['get','post','patch','delete','options','head']
    permission_classes = [IsAdminUser] 

    def get_permissions(self):
        if self.request.method in ['PATCH', 'DELETE']:
            return [IsAdminUser()]
        return [IsAuthenticated()]

    def create(self, request, *args, **kwargs):
        serializer = CreateOrderSerializer(data=request.data, context= {'user_id': self.request.user.id})
        serializer.is_valid(raise_exception=True)
        order = serializer.save()
        serializer = OrderSerializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return CreateOrderSerializer
        elif self.request.method == 'PATCH':
            return UpdateOrderSerializer
        return OrderSerializer
    
    def get_queryset(self):
        user = self.request.user
        if self.request.user.is_staff:
            return Order.objects.all()
        
        customer_id = Customer.objects.only('id').get(user_id=user.id)
        return Order.objects.filter(customer_id=customer_id)       



class OrderItemViewset(ModelViewSet):
    queryset = OrderItem.objects.select_related('products').all()
