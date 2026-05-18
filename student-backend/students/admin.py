from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser, StudentProfile


# Register CustomUser in Django admin with extra fields visible.
@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    # Add our two custom flags to the user edit screen.
    fieldsets = UserAdmin.fieldsets + (
        ("Student flags", {"fields": ("is_student", "is_approved")}),
    )
    list_display = ("username", "email", "is_student", "is_approved", "is_staff")
    list_filter = ("is_student", "is_approved", "is_staff")


# Register StudentProfile so admins can browse profiles in Django admin too.
@admin.register(StudentProfile)
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ("name", "user", "course", "branch", "course_year")
    search_fields = ("name", "user__username")
