from django.db import models
from django.contrib.auth.models import AbstractUser

from enum import Enum
from utils.enums import BaseEnum

class UserTypeEnum(BaseEnum):
  ORDINARY = 'ORDINARY'
  MERCHANT = 'MERCHANT'

class User(AbstractUser):
  user_type = models.CharField(max_length=255, choices=UserTypeEnum.choices(), default=UserTypeEnum.ORDINARY.value)
  
  def __str__(self):
    return self.username
  