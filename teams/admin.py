from django.contrib import admin
from .models import Team
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name', 'registration__date_joined','ctfd_team_id','registration__team_name', 'created_at')
    readonly_fields = ('ctfd_team_id', 'created_at')
    search_fields = ('team_name',)
# Register your models here.
