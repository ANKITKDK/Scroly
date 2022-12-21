from django.contrib import admin
from .models import LoginProfile, UserType,Login
# Register your models here.

admin.site.register(UserType)
admin.site.register(LoginProfile)

admin.site.register(Login)
