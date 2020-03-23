from django.contrib import admin
from import_export.admin import ImportExportMixin

from post.models import Post, PostImage


@admin.register(Post)
class StoreAdmin(ImportExportMixin, admin.ModelAdmin):
    pass


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass


