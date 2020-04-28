from django.contrib import admin

from import_export.admin import ImportExportMixin

from location.models import Locate


@admin.register(Locate)
class LocateAdmin(ImportExportMixin, admin.ModelAdmin):
    list_display = ('id', 'dong', 'address', 'longitude', 'latitude')
