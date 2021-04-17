from django.db import models

class BaseModel(models.Model):
  ''' 
    An abstract base Model for auto creating timestamps
  '''
  created_at = models.DateTimeField(auto_now_add=True)
  updated_at = models.DateTimeField(auto_now=True)
  class Meta:
    abstract=True
