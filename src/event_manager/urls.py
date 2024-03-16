from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from rest_framework.routers import DefaultRouter

from events.views import EventViewSet

drf_router_v1 = DefaultRouter()
drf_router_v1.register(r'events', EventViewSet, basename='events')

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # API views
    path('api/v1/', include(drf_router_v1.urls)),

    # Djoser (register + login/refresh/validate token endpoints)
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]

if settings.DEBUG:
    urlpatterns += [

        # Openapi3 UI
        path('api-schema.yaml', SpectacularAPIView.as_view(), name='schema'),
        path('docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    ]
