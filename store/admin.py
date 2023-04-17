from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book, UserBookRelation


@admin.register(Book)
class BookAdmin(ModelAdmin):
    """How and what will be reflected in the admin panel"""

    list_display = ('name', 'price',)
    fields = ('name', 'price', 'author_name', 'description', 'owner')
    list_filter = ('price',)
    search_fields = ('name',)
    ordering = ('-name', '-price',)


@admin.register(UserBookRelation)
class UserBookRelationAdmin(ModelAdmin):
    pass
