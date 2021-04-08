from rest_framework import serializers

from users.models import User

class UserSerializer(serializers.ModelSerializer):
  user_type = serializers.CharField(max_length=255, read_only=True)
  password = serializers.CharField(max_length=255, write_only=True)
  
  class Meta:
    model = User
    fields = ('id', 'username', 'user_type', 'password',
                  'first_name', 'last_name')