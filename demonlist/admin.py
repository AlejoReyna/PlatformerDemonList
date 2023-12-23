"""DemonList models."""

# Django
from django.contrib import admin

# Models
from demonlist.models import Demon, Record


@admin.register(Demon)
class DemonAdmin(admin.ModelAdmin):
    """Demon admin."""

    list_display = ('id', 'level', 'creator', "position")
    search_fields = ('level',)
    list_filter = ('created', 'modified')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Record admin."""

    list_display = ('id', 'demon', 'player')
    search_fields = ('demon', 'player')
    list_filter = ('datetime_submit', 'datetime_modified')
