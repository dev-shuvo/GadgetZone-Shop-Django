from django.contrib import admin
from .models import User, UserProfile
from django.contrib.auth.admin import UserAdmin


class UserAdmin(UserAdmin):
    list_display = (
        "email",
        "first_name",
        "last_name",
        "username",
        "last_login",
        "date_joined",
        "is_active",
    )
    list_display_links = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined")
    ordering = ("-date_joined",)

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


class UserProfileAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "country",
        "state",
        "city",
        "pin_code",
        "created_at",
        "modified_at",
    )
    list_filter = (
        "country",
        "state",
        "city",
        "pin_code",
    )
    ordering = ("created_at",)
    search_fields = (
        "user__username__icontains",
        "user__email__icontains",
    )


admin.site.register(User, UserAdmin)
admin.site.register(UserProfile, UserProfileAdmin)
