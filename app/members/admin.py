from django.contrib import admin
from .models import User


@admin.register(User)
class MembersAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'avatar']
    list_filter = ['username', 'created', 'updated']
    search_fields = ['username', 'phone']
    fields = ('uid', 'username', 'phone', 'avatar','created', 'updated')
    readonly_fields = ("created", 'updated',)