from django.test import TestCase, Client
from django.urls import reverse
from rest_framework.test import APIRequestFactory
from users.models import User
from books.models import Book, Category
from books.views import BookViewSet
from books.serializers import BookSerializer

client = Client()
class GetAllBooksTest(TestCase):
  def setUp(self):
    # setup api request factory
    self.factory = APIRequestFactory()
    # create a merchant user
    merchant_user = User.objects.create(user_type="MERCHANT")
    #create some nested categories
    category_one = Category.objects.create(name='test_category', parent=None)
    category_Two = Category.objects.create(name='test_category', parent=category_one)
    category_Three = Category.objects.create(name='test_category', parent=category_Two)

    # create some new books
    Book.objects.create(title='book_test_1', price=230, merchant=merchant_user, category=category_one)

  def test_get_all_books(self):
    request = self.factory.get('/api/books/')
    view = BookViewSet.as_view({"get": "list"})
    response = view(request)
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    self.assertEqual(response.status_code, 200)
    self.assertEqual(response.data, serializer.data)

class GetSingleBookTest(TestCase):
  def setUp(self):
    # setup api request factory
    self.factory = APIRequestFactory()
    # create a merchant user
    merchant_user = User.objects.create(user_type="MERCHANT")
    #create nested categories
    category_one = Category.objects.create(name='test_category', parent=None)
    category_Two = Category.objects.create(name='test_category', parent=category_one)
    category_Three = Category.objects.create(name='test_category', parent=category_Two)
    # create new books
    Book.objects.create(title='book_test_1', price=230, merchant=merchant_user, category=category_one)
    Book.objects.create(title='book_test_2', price=200, merchant=merchant_user, category=category_Two)
    Book.objects.create(title='book_test_3', price=110, merchant=merchant_user, category=category_Three)

  def test_get_single_book(self):
    request = self.factory.get('/api/books/',)
    view = BookViewSet.as_view({"get": "retrieve"})
    response = view(request, pk=3)
    book = Book.objects.filter(pk=3).first()
    serializer = BookSerializer(book)

    self.assertEqual(response.data, serializer.data)
    self.assertEqual(response.status_code, 200)




  