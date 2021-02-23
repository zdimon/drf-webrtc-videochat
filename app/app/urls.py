from django.contrib import admin
from django.urls import path
from webrtc.views import index
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from webrtc.views import OfferView

schema_view = get_schema_view(
    openapi.Info(
        title="API",
        default_version='v1',
        description=''' Documentation
        The `ReDoc` view can be found [here](/doc).
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
    path('test', index),
    path('admin/', admin.site.urls),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('doc', schema_view.with_ui('redoc', cache_timeout=0), name='schema-doc'),
]
