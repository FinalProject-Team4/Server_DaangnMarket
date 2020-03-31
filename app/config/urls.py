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

    # drf-yasg
    path('swagger<str:format>', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('docs/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

urlpatterns += static(
    # URL앞부분이 /media/이면
    prefix=settings.MEDIA_URL,
    # document_root위치에서 나머지 path에 해당하는 파일을 리턴
    document_root=settings.MEDIA_ROOT,
)

if settings.DEBUG:
    # django-debugtoolbar
    import debug_toolbar

    urlpatterns = [
        path('__debug__/', include(debug_toolbar.urls)),
    ] + urlpatterns
