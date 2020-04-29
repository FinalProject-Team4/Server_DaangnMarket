import os

from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from .docs_views import schema_view
from config import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('location/', include('location.urls')),
    path('post/', include('post.urls')),
    path('members/', include('members.urls')),
    path('fcm/', include('notification.urls')),
    path('chat/', include('chat.urls')),

    # drf-yasg
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if os.environ.get('DJANGO_SETTINGS_MODULE') != 'config.settings.production':
    # django-debugtoolbar
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns

    # local media
    urlpatterns += static(prefix=settings.dev.MEDIA_URL, document_root=settings.dev.MEDIA_ROOT, )
