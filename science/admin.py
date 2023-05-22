from django.contrib import admin
from .models import *


def form_list_fields(model, exclude: set) -> list:
    fields = set((field.name for field in model._meta.local_fields))
    fields.difference_update(exclude)
    return list(fields)


@admin.register(Science)
class ScienceAdmin(admin.ModelAdmin):
    list_display = form_list_fields(model=Science, exclude={"content", })
    list_display_links = ('title', 'slug')
    ordering = ('id', )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = form_list_fields(model=Category, exclude={'content', })
    list_display_links = ('title', 'slug')
    ordering = ('id', )


@admin.register(Formula)
class FormulaAdmin(admin.ModelAdmin):
    list_display = form_list_fields(model=Formula, exclude={'content', })
    list_display_links = ('title', 'slug')
    ordering = ('id', )
