from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ("Classification", {"fields": ("clearance",)}),
        ("Attributes", {"fields": ("access_attributes",)}),
    )
    list_display = ("username", "email", "clearance")
    search_fields = ("username", "email")
    list_filter = ("clearance",)
    filter_horizontal = ("access_attributes",)


admin.site.register(User, CustomUserAdmin)
