from django.contrib import admin
from django.urls import path, include
from reunion.views import index
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index),
    path('admin/', admin.site.urls),
    path('accounts/', include([
        path('', include('django.contrib.auth.urls')),
        path('register/', include('reunion.urls')),

    ])),
]

if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)