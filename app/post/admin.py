from django.contrib import admin
from import_export.admin import ImportExportMixin

from post.models import Post, PostImage, PostLike


@admin.register(Post)
class PostAdmin(ImportExportMixin, admin.ModelAdmin):
    filter_horizontal = ('showed_locates',)


@admin.register(PostImage, PostLike)
class PostImageAdmin(admin.ModelAdmin):
    list_display = ('image_name', 'post')

    def image_name(self, obj):
        return obj.photo.name

    image_name.short_description = 'Image File Name'
