from django.db import models

class Book(models.Model):
  def __str__(self):
    return self.title

  title = models.CharField(max_length=255)
  price = models.IntegerField(default=0)
  category = models.ForeignKey('Category', on_delete=models.CASCADE)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Category(models.Model):
  def __str__(self):
    return self.name
  
  name = models.CharField(max_length=255)
  parent = models.ForeignKey('Category', on_delete=models.PROTECT,
                    related_name='children', blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Author(models.Model):
  def __str__(self):
      return self.name
  
  name = models.CharField(max_length=255)
  created_at = models.DateTimeField(auto_now_add=True, blank=True, null=True)
  updated_at = models.DateTimeField(auto_now=True, blank=True, null=True)


class Book_Author(models.Model): # seperately Implementing m2m relationship
  def __str__(self):
      return self.book + " | " + self.author
  
  book = models.ForeignKey(Book, on_delete=models.CASCADE)
  author = models.ForeignKey(Author, on_delete=models.CASCADE)

  
  