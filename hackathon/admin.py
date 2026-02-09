from django.contrib import admin
from .models import Project


class ProjectAdmin(admin.ModelAdmin):
    list_display = ('team', 'project_link', 'total_score', 'submission_time')
    list_filter = ('submission_time',)
    search_fields = ('team__team_name',)
    readonly_fields = ('submission_time',)
    ordering = ('-total_score', '-submission_time')
    
    list_editable = ('total_score',)
    
    actions = ['reset_scores', 'export_scores_csv']

    @admin.action(description="🔄 Reset all scores to 0")
    def reset_scores(self, request, queryset):
        updated = queryset.update(total_score=0)
        self.message_user(request, f"Reset scores for {updated} projects")