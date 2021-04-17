from django.db import models
from users.models import User
from utils.models import BaseModel
class Book(BaseModel):
  def __str__(self):
    return self.title

  title = models.CharField(max_length=255)
  price = models.IntegerField(default=0)
  merchant = models.ForeignKey(User, on_delete=models.CASCADE)
  category = models.ForeignKey('Category', on_delete=models.CASCADE)
  tags = models.ManyToManyField("Tag", related_name='books', blank=True)

  @property
  def authors(self):
    book_author_qs = Book_Author.objects.filter(book__title=self.title)
    authors = [obj.author for obj in book_author_qs]
    return authors
    

class Category(BaseModel):
  def __str__(self):
    return self.name
  
  name = models.CharField(max_length=255)
  parent = models.ForeignKey('Category', on_delete=models.PROTECT,
                    related_name='children', blank=True, null=True)
  class Meta:
    verbose_name_plural = "categories"


class Author(BaseModel):
  def __str__(self):
      return self.name
  
  name = models.CharField(max_length=255)


class Tag(BaseModel):
  def __str__(self):
    return self.name

  name = models.CharField(max_length=50)
      

class Book_Author(models.Model): # seperately Implementing m2m relationship
  def __str__(self):
    return self.book.title + " | " + self.author.name
  
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, on_delete=models.CASCADE)

  
  