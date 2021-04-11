from books.models import Book, Author, Book_Author, Category, Tag
from users.models import User, UserTypeEnum
import re

def is_valid_authors(*, author_ids):
  # check if author_ids are list of integer ids
  return author_ids is not None and isinstance(author_ids, list) and all(isinstance(a_id, (int)) for a_id in author_ids)

def add_book_item(*, title, price, category, tags, author_ids, merchant_id):
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

  # create book tags:
  if tags is None:
    return 400, {"tags": ["is required."]}
  #split tags by space, comma, and period characters but leave numbers
  split_tags = re.split("\s|(?<!\d)[,.](?!\d)", tags)

  book_item = Book.objects.create(title=title, category=category_item, price=price, merchant=merchant)
  for tag_name in split_tags:
    exist_tag = Tag.objects.filter(name=tag_name).first()
    if exist_tag:
      book_item.tags.add(exist_tag)
    else:
      created_tag = Tag.objects.create(name=tag_name)
      book_item.tags.add(created_tag)
  book_item.save()
  # create object of book_author model from implementing m2m relationship
  for author in valid_authors:
    Book_Author.objects.create(book=book_item, author=author)
  
  return 201, book_item
    
def update_book_item(*, request, instance, title, price, category, author_ids, merchant_id, tags=None):
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
  book_authors = [book_author.author_id for book_author in Book_Author.objects.filter(book=instance)]

  for author_id in author_ids:
    author = Author.objects.filter(id=author_id).first()
    if author is not None:
      valid_authors.append(author)
      if author.id not in book_authors:
        Book_Author.objects.create(book=instance, author=author)

  valid_author_ids = [author.id for author in valid_authors]

  for book_author in book_authors:
    if book_author not in valid_author_ids:
      Book_Author.objects.filter(book=instance, author=book_author).delete()


  if len(valid_authors) < 1:
    return 406, {"author_ids": ["is not valid"]}

  # all valid
  instance.title = title or instance['title']
  instance.price = price or instance['price']
  instance.category = category_item or instance['category']

  # adding tags due update:
  if tags:
    split_tags = re.split("\s|(?<!\d)[,.](?!\d)", tags)
    for tag_name in split_tags:
      exist_tag = Tag.objects.filter(name=tag_name).first()
      tag_alredy_in_book = instance.tags.filter(name=tag_name).first()
      if tag_alredy_in_book:
        continue
      elif exist_tag:
        instance.tags.add(exist_tag)
      else:
        created_tag = Tag.objects.create(name=tag_name)
        instance.tags.add(created_tag)

  instance.save()
  return 200, {"ok": "update successfully"}