# tokens/admin.py

from django.contrib import admin
from .models import Token, TokenSubmission
import secrets
import string
import hashlib

@admin.register(Token)
class TokenAdmin(admin.ModelAdmin):
    list_display = ('base_points', 'created_at', 'submission_count')
    list_filter = ('base_points', 'created_at')
    ordering = ('-created_at',)
    readonly_fields = ('token_hash', 'created_at')
    
    def submission_count(self, obj):
        return obj.submissions.count()
    submission_count.short_description = 'Submissions'
    
    fieldsets = (
        ('Token Info', {
            'fields': ('base_points', 'token_hash', 'created_at')
        }),
    )


@admin.register(TokenSubmission)
class TokenSubmissionAdmin(admin.ModelAdmin):
    list_display = ('team', 'token_points', 'submitted_at')
    list_filter = ('submitted_at', 'token__base_points')
    search_fields = ('team__team_name',)
    readonly_fields = ('team', 'token', 'submitted_at')
    ordering = ('-submitted_at',)
    
    def token_points(self, obj):
        return f"{obj.token.base_points} pts"
    token_points.short_description = 'Points'
    
    def has_add_permission(self, request):
        return False  # Tokens can only be submitted via API