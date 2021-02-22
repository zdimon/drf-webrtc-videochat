from django.contrib import admin
from .models import UserProfile, UserConnection

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['login', 'is_online']

@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'sid']
