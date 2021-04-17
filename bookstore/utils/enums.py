from enum import Enum

class BaseEnum(Enum):
  @classmethod
  def choices(cls):
    return [(i.value, i.name) for i in cls]