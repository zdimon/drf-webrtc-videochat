from django.contrib import admin
from django.urls import path
from webrtc.views import index, accept
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from webrtc.views import OfferView, CallView, AcceptView, DeclineView

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description=''' Documentation
           [Sender page](/sender).
           [Resiver page](/reciever).
        ''',
        terms_of_service="https://www.google.com/policies/terms/",
        contact=openapi.Contact(email="zdimon77@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('offer', OfferView.as_view()),
    path('call', CallView.as_view()),
    path('accept', AcceptView.as_view()),
    path('decline', DeclineView.as_view()),
    path('sender', index),
    path('reciever', accept),
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-doc'),
]
