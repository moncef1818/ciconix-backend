from celery import shared_task
from .models import Team

@shared_task(bind=True)
def sync_team_to_ctfd_task(self, team_id):
    """Background CTFd sync with more retries"""
    try:
        team = Team.objects.get(id=team_id)
        # Try sync again
        ctfd_id = team.sync_to_ctfd(team.team_password)
        return f"Team {team.team_name}: CTFd ID {ctfd_id}"
    except Team.DoesNotExist:
        return "Team not found"