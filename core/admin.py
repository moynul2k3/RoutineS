# admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import UserAccount

class UserAccountAdmin(BaseUserAdmin):
    ordering = ['email']
    list_display = ['email', 'name', 'REG_no', 'is_staff']
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal Info', {'fields': ('name', 'REG_no', 'university', 'department', 'batch')}),
        ('Permissions', {'fields': ('is_active', 'is_CR', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'REG_no', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'REG_no', 'university', 'department')

admin.site.register(UserAccount, UserAccountAdmin)
