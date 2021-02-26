from django.contrib import admin
from .models import UserProfile, UserConnection, Sdp, Ice

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['login', 'is_online']

@admin.register(UserConnection)
class UserConnectionAdmin(admin.ModelAdmin):
    list_display = ['user', 'sid']


@admin.register(Sdp)
class SdpAdmin(admin.ModelAdmin):
    list_display = ['from_user', 'from_user_sdp','to_user', 'to_user_sdp']


@admin.register(Ice)
class IceAdmin(admin.ModelAdmin):
    list_display = ['sdp', 'ice']
