# Django
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin

# Models
from django.contrib.auth.models import User
from users.models import Profile, Country

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    # Profile admin
    list_display = ("pk", "user", "verified", "list_points", "country")
    list_display_links = ("pk", "user")
    list_editable = ("list_points", "country")
    search_fields = ("user__username", "user__email", "user__first_name", "user__last_name", "phone")
    list_filter = ("user__is_active", "user__is_staff", "created", "modified")
    fieldsets = (
        ("Profile", {"fields": ("user", "picture")}),
        ("Extra info", {"fields": (("youtube_channel", "phone"), "bio", "country", "list_points", "followers", "dark_mode", "verified", "discord")}),
        ("Metadata", {"fields": ("created", "modified")}))
    readonly_fields = ("created", "modified")

class ProfileInline(admin.StackedInline):
    # Conexión con el Profile admin (para User admin)
    model = Profile
    can_delete = False
    verbose_name_plural = "profiles"

class UserAdmin(BaseUserAdmin):
    # Agrega el Profile admin al User admin
    inlines = (ProfileInline,)
    list_display = ("id", "username", "email", "is_active", "display_groups")

    def display_groups(self, obj):
        return ", ".join([group.name for group in obj.groups.all()])

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    """Country admin."""

    list_display = ('id', 'country', 'list_points', 'picture')
    list_editable = ("picture",)
    search_fields = ('country',)
    list_filter = ('country',)
