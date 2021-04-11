from rest_framework import serializers
from cart_api.models import Cart, Order

class CartSerializer(serializers.ModelSerializer):
  class Meta:
      model = Cart
      fields = ('id', 'items','user')

class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('id', 'items','cart')