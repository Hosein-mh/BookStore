from django.db import models
from django.contrib.auth.models import AbstractUser

from enum import Enum

class UserTypeEnum(Enum):
  ORDINARY = 'ORDINARY'
  MERCHANT = 'MERCHANT'

  @classmethod
  def choices(cls):
    return [(i.name, i.value) for i in cls]


class User(AbstractUser):
  user_type = models.CharField(max_length=255, choices=UserTypeEnum.choices(), default=UserTypeEnum.ORDINARY.value)
  
  def __str__(self):
    return self.username
  