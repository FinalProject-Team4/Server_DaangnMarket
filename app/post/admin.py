from django.contrib import admin
from import_export.admin import ImportExportMixin

from post.models import Post, PostImage


@admin.register(Post)
class PostAdmin(ImportExportMixin, admin.ModelAdmin):
    filter_horizontal = ('showed_locate',)


@admin.register(PostImage)
class PostImageAdmin(admin.ModelAdmin):
    pass
