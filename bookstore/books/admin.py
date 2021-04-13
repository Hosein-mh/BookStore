from django.contrib import admin
from django.contrib.auth.models import Group

from books.models import Book, Category, Author, Book_Author, Tag

class BookAdmin(admin.ModelAdmin):
  list_display = ('title','authors', 'created_at')
  list_filter = ('created_at',)
  search_fields = ('title', 'tags__name')
  ordering = ('created_at',)

admin.site.register(Book, BookAdmin)
admin.site.register(Category)
admin.site.register(Author)
admin.site.register(Book_Author)
admin.site.register(Tag)

admin.site.unregister(Group)

admin.site.site_header = 'Book Store admin dashboard'

