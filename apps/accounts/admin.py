from django.contrib import admin
from .models import User
from django.contrib.auth.admin import UserAdmin
# Register your models here.

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ("username", "email", "is_staff", "is_active", "created_at")
    list_filter = ("is_staff", "is_active")
    search_fields = ("username", "email")
    ordering = ("-created_at", )