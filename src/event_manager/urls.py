from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Djoser (register + login/refresh/validate token endpoints)
    path('api/v1/', include('djoser.urls')),
    path('api/v1/', include('djoser.urls.jwt')),
]
