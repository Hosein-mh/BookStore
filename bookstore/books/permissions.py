from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import UserTypeEnum


class IsAdminOrReadOnly(BasePermission):
  def has_permission(self, request, view):
    ''' 
      Only admin can edit authors 
      read permission to anyone
    '''
    if request.method in SAFE_METHODS:
      return True
    return request.user.is_authenticatd and request.user.is_staff
class IsMerchantOrReadOnly(BasePermission):
  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    return request.user.is_authenticated and \
      request.user.user_type == UserTypeEnum.MERCHANT.value

  def has_object_permission(self, request, view, obj):
    return request.user == obj.merchant

class isAdminOrMerchantOrReadOnly(BasePermission):

  def has_permission(self, request, view):
    if request.method in SAFE_METHODS:
      return True
    else:
      return request.user.is_authenticated and \
        (request.user.is_staff or \
        request.user.user_type == UserTypeEnum.MERCHANT.value)
      