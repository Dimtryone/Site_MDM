from django.contrib.auth import authenticate
from rest_framework import serializers
from .models import *


class SizeSerializer(serializers.ModelSerializer):
    size = serializers.CharField()
    class Meta:
        model = Size
        fields = ('size',)

class ProductSerializer(serializers.ModelSerializer):

    sizes = SizeSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ('product_id', 'color', 'sizes', 'amount', 'size', 'pk')

class OrderStatusSerializer(serializers.ModelSerializer):
    name_status = serializers.CharField()
    order_id = serializers.IntegerField()
    name = serializers.CharField(source='user.name')
    last_name = serializers.CharField(source='user.last_name')

    class Meta:
        model = OrderStatus
        fields = ['name_status', 'order_id', 'name', 'last_name']

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = "__all__"


class OrderSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(many=True, read_only=True)
    #queryset=Product.objects.all(), read_only=True)
    status = serializers.StringRelatedField(many=True, read_only=True)
    user = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        model = Order
        fields = ('id', 'adress', 'payment_method', 'description', 'product',
                  'status', 'user')

class OrderProductSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    order = serializers.PrimaryKeyRelatedField(queryset=Order.objects.all())
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())

    class Meta:
        model = OrderProduct
        fields = ('order', 'product', 'count',  'id')


    def validate(self, data):
        order_id = self.context['request'].data.get('order_id')
        product_id = self.context['request'].data.get('product_id')

        if OrderProduct.objects.filter(order=order_id, product=product_id).exists():
            raise serializers.ValidationError("Запись уже существует")

        return data

class MyAuthTokenSerializer(serializers.Serializer):
    '''Для получения токенов'''
    email = serializers.CharField()
    password = serializers.CharField()

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'), email=email, password=password)

            if not user:
                msg = 'Unable to authenticate with provided credentials'
                raise serializers.ValidationError(msg, code='authentication')

        else:
            msg = 'Must include "email" and "password".'
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


    # def validate(self, data):
    #     # Добавьте валидацию на уникальность связи между Order и Product
    #     if OrderProduct.objects.filter(order=data['order'], product=data['product']).exists():
    #         raise serializers.ValidationError('This order already contains this product')
    #     return data
# class OrderProductSerializer(serializers.ModelSerializer):
#     id = serializers.IntegerField(read_only=True)
#     product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
#
#     class Meta:
#         model = OrderProduct
#         fields = ('id', 'product', 'count')
#
#     def validate(self, data):
#         # Добавьте валидацию на уникальность связи между Order и Product
#         if OrderProduct.objects.filter(order=self.context['order'], product=data['product']).exists():
#             raise serializers.ValidationError('This order already contains this product')
#         return data
#
#     def create(self, validated_data):
#         order = self.context['order']
#         product = validated_data.pop('product')
#         count = validated_data.pop('count')
#         order_product = OrderProduct.objects.create(order=order, product=product, count=count)
#         return order_product


# class OrderProductSerializer(serializers.ModelSerializer):
#
#     class Meta:
#         model = OrderProduct
#         fields = ['id', 'count', 'product', 'order']
#
#     def validate(self, data):
#         order_id = self.context['request'].data.get('order_id')
#         product_id = self.context['request'].data.get('product_id')
#
#         if OrderProduct.objects.filter(order=order_id, product=product_id).exists():
#             raise serializers.ValidationError("Запись уже существует")

# class OrderProductSerializer(serializers.ModelSerializer):
#
#     def validate(self, data):
#         order_id = self.context['request'].data.get('order_id')
#         product_id = self.context['request'].data.get('product_id')
#
#         if OrderProduct.objects.filter(order_id=order_id, product_id=product_id).exists():
#             raise serializers.ValidationError("Запись уже существует")
#
#         return data
#
#     class Meta:
#         model = OrderProduct
#         fields = ('count', 'order_id', 'product_id')
#
#     def validate_count(self, value):
#         if value <= 0:
#             raise serializers.ValidationError("Count must be greater than 0")
#         return value
    #
    # def validate(self, data):
    #     if OrderProduct.objects.filter(order=data['order'], product=data['product']).exists():
    #         raise serializers.ValidationError('This order already contains this product')
    #     return data
    #
    # class Meta:
    #     model = OrderProduct
    #     fields = ['id', 'order', 'product', 'count']
