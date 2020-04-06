from django.contrib import admin
from .models import User


@admin.register(User)
class MembersAdmin(admin.ModelAdmin):
    list_display = ['username', 'phone', 'avatar', 'created', 'updated']
    list_filter = ['username', 'created', 'updated']
