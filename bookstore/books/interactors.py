from books.models import Book, Author, Book_Author, Category

def add_book_item(*, title, price, category, author_ids):
  valid_authors = []
  message = ""

  try:
    category_item = Category.objects.get(id=category)
  except Category.DoesNotExist:
      return 404, None

  for author_id in author_ids:
    author = Author.objects.filter(id=author_id).first()
    if author is not None:
      valid_authors.append(author)
  
  if len(valid_authors) < 1:
    return 406, None

  book_item = Book.objects.create(title=title, category=category_item, price=price)
  # create object of book_author model from implementing m2m relationship
  for author in valid_authors:
    Book_Author.objects.create(book=book_item, author=author)
  
  return 201, book_item
    
