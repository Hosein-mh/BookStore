from books.models import Book, Author, Book_Author, Category
from users.models import User, UserTypeEnum

def is_valid_authors(*, author_ids):
  # check if author_ids are list of integer ids
  return author_ids is not None and isinstance(author_ids, list) and all(isinstance(a_id, (int)) for a_id in author_ids)

def add_book_item(*, title, price, category, author_ids, merchant_id):
  valid_authors = []
  message = ""

  try:
    merchant = User.objects.get(pk=merchant_id)
    if not merchant.user_type == UserTypeEnum.MERCHANT.value:
      return 400, None
    pass
  except User.DoesNotExist:
      return 400, None

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

  book_item = Book.objects.create(title=title, category=category_item, price=price, merchant=merchant)
  # create object of book_author model from implementing m2m relationship
  for author in valid_authors:
    Book_Author.objects.create(book=book_item, author=author)
  
  return 201, book_item
    
def update_book_item(*, request, instance, title, price, category, author_ids, merchant_id):
  valid_authors = []
  if merchant_id is None:
    content = {"merchant_id": ["is Required"]}
    return 400, content

  try:
    merchant = User.objects.get(pk=merchant_id)
    if not merchant.user_type == UserTypeEnum.MERCHANT.value:
      return 403, {"permission denied": "only merchant can update books"}
    pass
  except User.DoesNotExist:
      return 404, {"merchant": "Not found"}

  if request.user.user_type == UserTypeEnum.MERCHANT and merchant != request.user:
    return 403, {"merchant": ["your not the merchant of this book"]}

  if not is_valid_authors(author_ids=author_ids):
    content = {"author_ids": ["list of author_ids are required"]}
    return 400, content

  valid_authors = []
  try:
    category_item = Category.objects.get(id=category)
  except Category.DoesNotExist:
      return 404, None

  # get the past book authors and update them with new data
  book_authors = [book_author.author.id for book_author in Book_Author.objects.filter(book=instance)]

  for author_id in author_ids:
    author = Author.objects.filter(id=author_id).first()
    if author is not None:
      valid_authors.append(author)
      if author.id not in book_authors:
        Book_Author.objects.create(book=instance, author=author)

  # for book_author in book_authors:
  #   if book_author not in valid_authors:
  #     print('not in book authors:', book_author)
  #     Book_Author.objects.filter(book=instance, author=book_author).delete()



  
  if len(valid_authors) < 1:
    return 406, {"author_ids": ["is not valid"]}

  # all valid
  instance.title = title or instance['title']
  instance.price = price or instance['price']
  instance.category = category_item or instance['category']

  instance.save()
  saved_item = {
    "id": instance.id,
    "title": instance.title,
    "price": instance.price,
    "category": instance.category.id
  }
  return 200, saved_item