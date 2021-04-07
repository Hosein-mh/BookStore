from rest_framework import serializers

from books.models import Book, Author, Category, Book_Author


class CategorySerializer(serializers.ModelSerializer):
  class Meta:
    model = Category
    fields = ('id', 'name', 'parent')


class AuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Author
    fields = ('id', 'name')
  
class BookAuthorSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book_Author
    fields = ('id', 'book', 'author')

class BookSerializer(serializers.ModelSerializer):
  class Meta:
    model = Book
    fields = ('id', 'title', 'category', 'price')