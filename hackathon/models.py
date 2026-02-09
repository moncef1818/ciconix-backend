from django.db import models
from teams.models import Team

class Project(models.Model):

    team = models.OneToOneField(Team, on_delete=models.CASCADE, related_name='project')
    project_link = models.URLField(max_length=500)
    submission_time = models.DateTimeField(auto_now_add=True)
    total_score = models.IntegerField(default=0)

    class Meta:
        ordering = ['-submission_time']
    
    def __str__(self):
        return f"{self.team.team_name} - {self.project_link}"


# Create your models here.
