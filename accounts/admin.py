from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth import get_user_model

User = get_user_model()


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = ['email', 'full_name', 'username', 'exam_type', 'is_active', 'is_staff']
    list_filter = ['exam_type', 'is_active', 'is_staff']
    search_fields = ['email', 'full_name', 'username']
    ordering = ['email']

    # Fields shown when EDITING an existing user
    fieldsets = (
        (None, {'fields': ('email', 'username', 'password')}),
        ('Personal Info', {'fields': ('full_name', 'exam_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )

    # Fields shown when CREATING a new user (with password1/password2 for hashing)
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'username', 'full_name', 'exam_type', 'password1', 'password2'),
        }),
    )

