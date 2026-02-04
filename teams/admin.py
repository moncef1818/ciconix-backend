from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Team

@admin.register(Team)
class TeamAdmin(UserAdmin):
    list_display = ('email', 'team_name', 'is_staff', 'is_active', 'ctfd_team_id')
    list_filter = ('is_staff', 'is_active', 'is_superuser')
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Team Info', {'fields': ('team_name', 'ctfd_team_id')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'team_name', 'password1', 'password2'),
        }),
    )
    search_fields = ('email', 'team_name')
    ordering = ('email',)
