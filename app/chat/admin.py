from django.contrib import admin

# Register your models here.
from chat.models import Room, Message


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    pass


@admin.register(Message)
class RoomAdmin(admin.ModelAdmin):
    pass


