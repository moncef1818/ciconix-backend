from celery import shared_task
from .models import Team
import csv
import os
from django.conf import settings
from datetime import datetime

@shared_task(bind=True)
def sync_team_to_ctfd_task(self, team_id, plaintext_password):
    """Background CTFd sync with CSV update"""
    try:
        team = Team.objects.get(id=team_id)
        ctfd_id = team.sync_to_ctfd(plaintext_password)
        
        if ctfd_id:
            # Update CSV with successful sync
            _update_csv_status(team.team_name, ctfd_id)
        
        return f"Team {team.team_name}: CTFd ID {ctfd_id}"
    except Team.DoesNotExist:
        return "Team not found"

def _update_csv_status(team_name, ctfd_id):
    """Update CSV file with CTFd ID for previously failed syncs"""
    csv_dir = getattr(settings, 'TEAM_PASSWORDS_DIR', os.path.join(settings.BASE_DIR, 'secure_data'))
    csv_file = os.path.join(csv_dir, 'team_passwords.csv')
    
    if not os.path.exists(csv_file):
        return
    
    # Read all rows
    rows = []
    with open(csv_file, 'r', newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        rows.append(header)
        
        for row in reader:
            if row[0] == team_name and row[3] == 'PENDING':
                row[3] = str(ctfd_id)
                row[5] = 'Synced'
            rows.append(row)
    
    # Write back
    with open(csv_file, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerows(rows)