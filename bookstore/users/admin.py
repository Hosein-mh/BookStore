from django.contrib import admin

from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User

class UserAdmin(BaseUserAdmin):
    list_display = [
      'username',
      'email',
      'first_name',
      'last_name',
      'is_staff',
      'user_type'
    ]
    fieldsets = BaseUserAdmin.fieldsets + (
      ('Type', {'fields': ('user_type',)}),
    )

admin.site.register(User, UserAdmin)