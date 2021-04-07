from django.contrib import admin

from books.models import Book, Category, Author, Book_Author

# Register your models here.
admin.site.register(Book)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book_Author)

