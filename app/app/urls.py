from django.contrib import admin
from django.urls import path

from webrtc.views import index

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
]
