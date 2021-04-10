from django.shortcuts import render, get_object_or_404

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, SAFE_METHODS

from books.models import Book, Author, Category, Book_Author
from books.interactors import add_book_item, is_valid_authors, update_book_item
from books.permissions import IsMerchantOrReadOnly
from users.models import User, UserTypeEnum

from books.serializers import AuthorSerializer, BookSerializer, \
  CategorySerializer, BookAuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer
  # permission_classes = (IsAuthenticatedOrReadOnly,) #change it to isAsminOrMerchantOrReadOnly
  

class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = (IsAuthenticatedOrReadOnly,)


class BookViewSet(viewsets.ModelViewSet):
  serializer_class = BookSerializer
  permission_classes = (IsAuthenticatedOrReadOnly,)
  
  # Merchant only can see, update and delete his own books
  def get_queryset(self):
    """ access to staff users and merchants or read only """
    if self.request.method in SAFE_METHODS or self.request.user.is_staff:
      return Book.objects.all()
    else:
      books = Book.objects.filter(merchant=self.request.user)
      print("books for this merchant:", books)
      return books


  def create(self, request, *args, **kwargs):
    author_ids = request.data.get('author_ids', None)
    merchant = request.user
    permission_classes = (IsMerchantOrReadOnly,)


    # staff can add books for merchants
    if request.user.is_staff:
      merchant = request.data.get('merchant_id', None)

    if merchant is None:
      content = {"merchant_id": ["is Required"]}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)

    if not is_valid_authors(author_ids=author_ids):
      content = {"author_ids": ["list of author_ids are required"]}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)

    insert_status, item = add_book_item(
      title = request.data['title'],
      price = request.data['price'],
      category = request.data['category'],
      author_ids = author_ids,
      merchant_id = merchant
    )

    serializer = self.get_serializer(item)
    return Response(serializer.data, status=insert_status)


  def update(self, request, pk=None):
    permission_classes = (IsMerchantOrReadOnly,)

    try:
      instance = self.get_queryset().get(pk=pk)
    except Book.DoesNotExist:
      return Response({"Book": "no books founds"}, status=404)

    print('found book:', instance)

    insert_status, item = update_book_item(
      request = request,
      instance = instance,
      title = request.data['title'],
      price = request.data['price'],
      category = request.data['category'],
      author_ids = request.data['author_ids'],
      merchant_id = request.user.id
    )

    return Response(item, status=insert_status)


    


  
    













