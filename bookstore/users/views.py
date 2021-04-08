from django.shortcuts import render

from rest_framework import viewsets

from users.models import User
from users.serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
  queryset = User.objects.all()
  serializer_class = UserSerializer

  def get_queryset(self):
    print('self.request.user:',self.request.user)
    if self.request.user is None:
      return []
    else:
      return self.queryset.filter(username=self.request.user.username)
