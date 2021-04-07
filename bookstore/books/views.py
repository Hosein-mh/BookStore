from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, IsAdminUser

from books.models import Book, Author, Category, Book_Author

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
    return self.queryset

  # def create(self, request, *args, **kwargs):


