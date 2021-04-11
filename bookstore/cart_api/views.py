from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated

from cart_api.models import Cart
from books.models import Book
from cart_api.serializers import CartSerializer

class CartViewSet(viewsets.ModelViewSet):
  model = Cart
  serializer_class = CartSerializer

  def get_queryset(self,):
    return Cart.objects.filter(user=self.request.user)

  @action(['POST'], detail=False, url_path='add-to-cart', url_name='add_to_cart', permission_classes=[IsAuthenticated])
  def add(self, request, *args, **kwargs):
    cart_obj = self.get_queryset().first()
    item = self.request.data.get('item', None)

    if item is None:
      return Response({'item':'is required.'}, status=400)

    exist_items = [exist_item for exist_item in cart_obj.items.all()]
    new_items = []

    try:
      book_obj = Book.objects.get(id=item)
    except Book.DoesNotExist:
      return Response({"item": ["not found"]}, status=404)

    if book_obj not in exist_items:
      new_items.append(book_obj)
      
    items = exist_items + new_items
    cart_obj.items.set(items)
    cart_obj.save()

    serialized_cart = CartSerializer(cart_obj)
    return Response(serialized_cart.data, status=200)

  @action(['POST'], detail=False, url_path='remove-from-cart', url_name='remove_from_cart', permission_classes=[IsAuthenticated])
  def remove(self, request, *args, **kwargs):
    cart_obj = self.get_queryset().first()
    item = self.request.data.get('item', None)

    if item is None:
      return Response({'item':'is required.'}, status=400)

    try:
      book_obj = Book.objects.get(id=item)
    except Book.DoesNotExist:
      return Response({"item": ["not found"]}, status=404)

    exist_items = [exist_item for exist_item in cart_obj.items.all()]

    if book_obj in exist_items:
      exist_items.remove(book_obj)
    else:
      return Response({"message":"item not in cart."})
      
    cart_obj.items.set(exist_items)

    serialized_cart = CartSerializer(cart_obj)
    
    return Response(serialized_cart.data, status=200)

