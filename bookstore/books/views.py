from django.shortcuts import render, get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from books.filters import BookFilter

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAdminUser, IsAuthenticatedOrReadOnly, SAFE_METHODS

from books.models import Book, Author, Category, Book_Author, Tag
from books.interactors import add_book_item, is_valid_authors, update_book_item
from books.permissions import IsMerchantOrReadOnly, isAdminOrMerchantOrReadOnly, IsAdminOrReadOnly
from users.models import User, UserTypeEnum

from books.serializers import AuthorSerializer, BookSerializer, \
  CategorySerializer, BookAuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer
  permission_classes = (IsAdminOrReadOnly)
  

class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = (IsAdminOrReadOnly,)


class BookViewSet(viewsets.ModelViewSet):
  serializer_class = BookSerializer
  filter_backends = (DjangoFilterBackend,)
  filter_class = BookFilter
  
  # Merchant only can see, update and delete his own books
  def get_queryset(self):

    """ access to staff users and merchants or read only """
    if self.request.method in SAFE_METHODS or self.request.user.is_staff:
      self.queryset = Book.objects.all()
    else:
      self.queryset = Book.objects.filter(merchant=self.request.user)

    """ filter books based on tags from query_params"""
    tags = self.request.query_params.get('tags', None)
    if tags:
      tags = Tag.objects.filter(name__in=tags.split(' '))
      return self.queryset.filter(tags__in=tags)
    else: return self.queryset

  def get_permissions(self):
    if self.request.method == 'GET':
      permission_classes = [IsAdminOrReadOnly]
    else:
      permission_classes = [IsMerchantOrReadOnly]

    return [permission() for permission in permission_classes]



  def create(self, request, *args, **kwargs):
    author_ids = request.data.get('author_ids', None)
    merchant_id = request.user.id

    # staff can add books for merchants
    if request.user.is_staff:
      merchant_id = request.data.get('merchant_id', None)

    if not is_valid_authors(author_ids=author_ids):
      content = {"author_ids": ["list of author_ids are required"]}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)

    insert_status, item = add_book_item(
      title = request.data.get('title', None),
      price = request.data.get('price', None),
      category = request.data.get('category', None),
      tags = request.data.get('tags', None),
      author_ids = author_ids,
      merchant_id = merchant_id,
    )

    serializer = self.get_serializer(item)
    return Response(serializer.data, status=insert_status)


  def update(self, request, pk=None):
    try:
      instance = self.get_queryset().get(pk=pk)
    except Book.DoesNotExist:
      return Response({"Book": "no books founds in your merchant books"}, status=404)

    insert_status, item = update_book_item(
      request = request,
      instance = instance,
      title = request.data.get('title', instance.title),
      tags = request.data.get('tags', None),
      price = request.data.get('price', instance.price),
      category = request.data.get('category', instance.category),
      author_ids = request.data.get('author_ids', instance.authors),
      merchant_id = request.user.id
    )

    return Response(item, status=insert_status)


    


  
    













