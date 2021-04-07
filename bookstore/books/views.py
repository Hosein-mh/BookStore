from django.shortcuts import render

from rest_framework import viewsets, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from books.models import Book, Author, Category, Book_Author
from books.interactors import add_book_item

from books.serializers import AuthorSerializer, BookSerializer, \
  CategorySerializer, BookAuthorSerializer

class AuthorViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all()
  serializer_class = AuthorSerializer
  permission_classes = (IsAuthenticatedOrReadOnly,) #change it to isMerchantOrReadOnly

  def get_queryset(self):
    return super().get_queryset()
  

class CategoryViewSet(viewsets.ModelViewSet):
  queryset = Category.objects.all()
  serializer_class = CategorySerializer
  permission_classes = (IsAuthenticatedOrReadOnly,)


class BookViewSet(viewsets.ModelViewSet):
  queryset = Book.objects.all()
  serializer_class = BookSerializer
  permission_classes = (IsAuthenticatedOrReadOnly,)

  def get_queryset(self):
    return Book.objects.all()

  def create(self, request, *args, **kwargs):
    author_ids = request.data.get('author_ids', None)

    if author_ids is None or not isinstance(author_ids, list):
      content = {"author_ids": ["list of author_ids are required"]}
      return Response(content, status=status.HTTP_400_BAD_REQUEST)

    # if client do not send field what?
    insert_status, item = add_book_item(
      title = request.data['title'],
      price = request.data['price'],
      category = request.data['category'],
      author_ids = author_ids
    )

    serializer = self.get_serializer(item)
    return Response(serializer.data, status=insert_status)

  
  # def list(self, request, *args, **kwargs):
  #   queryset = self.get_queryset()
    











