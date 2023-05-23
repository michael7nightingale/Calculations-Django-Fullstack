from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = [field.name for field in User._meta.local_fields]
    list_display_links = ('username', 'id')
    ordering = ("id", )


@admin.register(Scientist)
class ScientistAdmin(admin.ModelAdmin):
    list_display = [field.name for field in Scientist._meta.local_fields]
    list_display_links = ('id', )
    ordering = ("id",)
