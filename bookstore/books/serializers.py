from rest_framework import serializers

from books.models import Book, Author, Category, Book_Author, Tag


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

class TagSerializer(serializers.ModelSerializer):
  class Meta:
    model = Tag
    fields = ('id', 'name')

class BookSerializer(serializers.ModelSerializer):
  authors = AuthorSerializer(many=True)
  tags = TagSerializer(read_only=True, many=True)

  class Meta:
    model = Book
    fields = ('id', 'title', 'tags', 'merchant', 'category', 'price', 'authors', 'created_at', 'updated_at')