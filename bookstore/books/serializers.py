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
  authors = serializers.SerializerMethodField()
  tags = TagSerializer(read_only=True, many=True)

  class Meta:
    model = Book
    fields = ('id', 'title', 'tags', 'merchant', 'category', 'price', 'authors', 'created_at', 'updated_at')
    

  def get_authors(self, obj):
    book_authors = Book_Author.objects.filter(book=obj)
    authors = []
    if len(book_authors) > 0 :
      authors = [AuthorSerializer(book_author.author).data for book_author in book_authors]
    return authors