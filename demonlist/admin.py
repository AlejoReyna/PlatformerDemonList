"""DemonList models."""

# Django
from django.contrib import admin
from django.contrib.auth.models import Group

# Models
from demonlist.models import Demon, Record, Changelog

class ProfileModFilter(admin.SimpleListFilter):
    title = 'Profile Mod'
    parameter_name = 'profile_mod'

    def lookups(self, request, model_admin):
        return (
            ('chucky_gd', 'chucky_gd'),
            ('Abr4h4M', 'Abr4h4M'),
            ('DoSh7t', 'DoSh7t'),
            ('GermánIglesario', 'GermánIglesario'),
            ('MSGUS', 'MSGUS'),
            ('Mechabrandon', 'Mechabrandon'),
            ('Ryexus', 'Ryexus'),
            ('IvanCrafter026', 'IvanCrafter026'),
            ('DiegoLix', 'DiegoLix'),
            ('Lunnagd', 'Lunnagd'),
            ('Alvaneder', 'Alvaneder'),
        )

    def queryset(self, request, queryset):
        if (self.value()):
            return queryset.filter(mod__user__username=self.value())

@admin.register(Demon)
class DemonAdmin(admin.ModelAdmin):
    """Demon admin."""

    list_display = ('id', 'level', 'creator', "position", "list_points", "verification_video_embed", "verification_video")
    search_fields = ('level',)
    list_filter = ('created', 'modified')

@admin.register(Record)
class RecordAdmin(admin.ModelAdmin):
    """Record admin."""

    list_display = ('id', 'demon', 'player', 'accepted', "mod", "mod_notes", "datetime_accepted")
    search_fields = ('player__user__username',)
    list_filter = ("demon", "accepted", ProfileModFilter, 'datetime_submit', 'datetime_accepted')

@admin.register(Changelog)
class ChangelogAdmin(admin.ModelAdmin):
    """Changelog admin."""

    list_display = ('id', 'demon', 'reason', 'position')
    search_fields = ('level',)
    list_filter = ("demon", 'datetime',)
