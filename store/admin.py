from django.contrib import admin
from django.contrib.admin import ModelAdmin

from store.models import Book


@admin.register(Book)
class BookAdmin(ModelAdmin):
    """How and what will be reflected in the admin panel"""

    list_display = ('name', 'price',)
    fields = ('name', 'price', 'description',)
    list_filter = ('price',)
    search_fields = ('name',)
    ordering = ('-name', '-price',)