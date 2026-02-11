from django.contrib import admin
from django.http import HttpResponse
import csv
from .models import Project
from io import StringIO

@admin.register(Project)  # ✅ THIS REGISTERS IT!
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('team', 'project_link', 'total_score', 'submission_time')
    list_filter = ('submission_time',)
    search_fields = ('team__team_name',)
    readonly_fields = ('submission_time',)
    ordering = ('-total_score', '-submission_time')
    
    list_editable = ('total_score',)
    
    # ✅ ACTIONS MUST BE IN actions LIST
    actions = ['reset_scores', 'export_scores_csv']  # ✅ NOW WORKS!

    @admin.action(description="🔄 Reset all scores to 0")
    def reset_scores(self, request, queryset):
        updated = queryset.update(total_score=0)
        self.message_user(request, f"Reset {updated} project(s) scores to 0", level='success')
        return

    @admin.action(description="📊 Export selected projects to CSV")
    def export_scores_csv(self, request, queryset):
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="projects_scores.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Team', 'Project Link', 'Total Score', 'Submission Time'])
        
        for project in queryset:
            writer.writerow([
                project.team.team_name if project.team else 'No Team',
                project.project_link,
                project.total_score,
                project.submission_time
            ])
        
        return response
