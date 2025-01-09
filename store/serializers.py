from decimal import Decimal
from rest_framework import serializers
from .models import CartItem, Product, Collection, Review, Cart


class CollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Collection
        fields = ['id', 'title','products_count']

    products_count = serializers.IntegerField(read_only=True)     


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'description', 'inventory', 'slug', 'unit_price', 'discount', 'collection']
   
    discount = serializers.SerializerMethodField(method_name='calculate_discount')
   #  collection = serializers.StringRelatedField()

    def calculate_discount(self, product: Product):
        return product.unit_price * Decimal(0.5) 
    
class SimpleProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'title', 'unit_price']    
    

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ['id', 'date', 'name', 'description']

    def create(self, validated_data):
        product_id = self.context['product_id']
        return Review.objects.create(product_id=product_id,**validated_data) 
    

class CartItemSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    total_price = serializers.SerializerMethodField(method_name='get_total_price')
    product = SimpleProductSerializer()

    def get_total_price(self, cart_item: CartItem):
        return cart_item.product.unit_price * cart_item.quantity
    
    class Meta:
        model = CartItem
        fields = ['id','product', 'quantity', 'total_price']    

class AddCartItemSerializer(serializers.ModelSerializer):
    product_id = serializers.IntegerField()

    def validate_product_id(self, value):
        if not Product.objects.filter(pk=value).exists():
            raise serializers.ValidationError('No such a product with a given id')
        return value


    def save(self, **kwargs):
        cart_id = self.context['cart_id']
        product_id = self.validated_data['product_id']
        quantity = self.validated_data['quantity']
        try:
            cart_item = CartItem.objects.get(cart_id=cart_id, product_id=product_id)
            cart_item.quantity += quantity
            cart_item.save()
            self.instance = cart_item
        except CartItem.DoesNotExist:
            self.instance = CartItem.objects.create(cart_id=cart_id, **self.validated_data)

        return self.instance    

    
    class Meta:
        model = CartItem
        fields = ['id', 'product_id', 'quantity']     


class UpdateCartItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = CartItem
        fields = ['quantity']           


class CartSerializer(serializers.ModelSerializer):
    id = serializers.UUIDField(read_only=True)
    items = CartItemSerializer(many=True, read_only=True)
    total_price = serializers.SerializerMethodField('get_total_price')

    def get_total_price(self, cart: Cart):
        return sum([item.product.unit_price * item.quantity for item in cart.items.all()])

    class Meta:
        model = Cart
        fields = ['id','items', 'total_price']

    
   