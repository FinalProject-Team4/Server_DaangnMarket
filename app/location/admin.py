from django.contrib import admin

from import_export.admin import ImportExportMixin

from location.models import Locate


@admin.register(Locate)
class StoreAdmin(ImportExportMixin, admin.ModelAdmin):
    pass

