from asyncio.log import logger
from django.contrib import admin

from .models import SpecialPassRegistration, BasicPassRegistration
from teams.models import Team
import csv
import os
from django.conf import settings
from datetime import datetime
from teams.tasks import _update_csv_status

        
@admin.register(SpecialPassRegistration)
class SpecialPassAdmin(admin.ModelAdmin):
    list_display = ('team_name',
                     'firstname1', 'lastname1', 'discord_id1',
                     'firstname2', 'lastname2', 'discord_id2',
                     'firstname3', 'lastname3', 'discord_id3',
                     'firstname4', 'lastname4', 'discord_id4',
                     'firstname5', 'lastname5', 'discord_id5',
                     'date_joined','is_approved')
    list_filter = ['school1', 'is_approved', 'date_joined']
    search_fields = ('team_name',
                    'firstname1', 'lastname1',
                    'firstname2', 'lastname2',
                    'firstname3', 'lastname3',
                    'firstname4', 'lastname4',
                    'firstname5', 'lastname5'
                    )

    actions = ['approve_registrations' , 'reject_registrations' , 'reject_all_registrations', 'export_as_csv']
    
    

    
    def save_model(self, request, obj, form, change):
        was_approved = obj.is_approved
        super().save_model(request, obj, form, change)
    
        if obj.is_approved and not Team.objects.filter(registration=obj).exists():
            secure_password = Team.generate_secure_password()
            
            # Create Django team
            team = Team.objects.create_user(
                email=obj.email1,
                team_name=obj.team_name,
                password=secure_password
            )
            team.registration = obj
            team.save()
    
            # 🔥 TRY CTFd sync (logs everything)
            logger.info(f"🔄 Attempting CTFd sync for {team.team_name}")
            ctfd_id = team.sync_to_ctfd(secure_password)
            
            # ✅ ALWAYS save CSV backup
            self._save_password_to_csv(team.team_name, obj.email1, secure_password, ctfd_id)
            
            if ctfd_id:
                message = f"✅ {team.team_name}\n🌐 CTFd ID: {ctfd_id}\n📝 Password → CSV"
            else:
                message = (f"✅ {team.team_name} created + CSV saved\n"
                          f"🔄 Check Django logs for CTFd error\n"
                          f"📋 Use 'Retry CTFd Sync' button")
                
            self.message_user(request, message, level='success')
        
    def _save_password_to_csv(self, team_name, email, password, ctfd_id):
        """Save team credentials to CSV file"""
        # Define CSV file path (in a secure location)
        csv_dir = getattr(settings, 'TEAM_PASSWORDS_DIR', os.path.join(settings.BASE_DIR, 'secure_data'))
        os.makedirs(csv_dir, exist_ok=True)
        
        csv_file = os.path.join(csv_dir, 'team_passwords.csv')
        
        # Check if file exists to write header
        file_exists = os.path.isfile(csv_file)
        
        with open(csv_file, 'a', newline='', encoding='utf-8') as f:
            writer = csv.writer(f)
            
            # Write header if new file
            if not file_exists:
                writer.writerow([
                    'Team Name', 
                    'Email', 
                    'Password', 
                    'CTFd ID', 
                    'Created At',
                    'Status'
                ])
            
            # Write team data
            writer.writerow([
                team_name,
                email,
                password,
                ctfd_id if ctfd_id else 'PENDING',
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'Synced' if ctfd_id else 'Sync Failed'
            ])
# Add manual sync action
    @admin.action(description="🔄 Retry CTFd Sync (uses CSV passwords)")
    def retry_ctfd_sync_from_csv(self, request, queryset):
        """Retry sync for teams that failed, using CSV stored passwords"""
        import csv

        csv_dir = getattr(settings, 'TEAM_PASSWORDS_DIR', os.path.join(settings.BASE_DIR, 'secure_data'))
        csv_file = os.path.join(csv_dir, 'team_passwords.csv')

        if not os.path.exists(csv_file):
            self.message_user(request, "❌ CSV file not found!", level='error')
            return

        # Read passwords from CSV
        password_map = {}
        with open(csv_file, 'r', newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                password_map[row['Team Name']] = row['Password']

        fixed = 0
        failed = []

        # 🔥 FIXED: Get TEAMS via registration (not SpecialPassRegistration!)
        for registration in queryset:
            if hasattr(registration, 'team') and registration.team:  # ✅ Check team exists
                team = registration.team
                # ✅ NOW filter on TEAM.ctfd_team_id (correct model!)
                if not team.ctfd_team_id:  # ✅ team.ctfd_team_id__isnull=True equivalent
                    if team.team_name in password_map:
                        password = password_map[team.team_name]
                        ctfd_id = team.sync_to_ctfd(password)

                        if ctfd_id:
                            fixed += 1
                            # Update CSV
                            _update_csv_status(team.team_name, ctfd_id)
                        else:
                            failed.append(team.team_name)
                    else:
                        failed.append(f"{team.team_name} (not in CSV)")
                else:
                    failed.append(f"{team.team_name} (already synced)")
            else:
                failed.append(f"{registration.team_name} (no Django team)")

        message = f"✅ Synced {fixed} teams to CTFd!"
        if failed:
            message += f"\n❌ Failed: {', '.join(failed[:5])}"  # Limit list length

        self.message_user(request, message, level='success' if fixed > 0 else 'warning')

    # Add this to actions list
    actions = ['approve_registrations', 'reject_registrations', 'reject_all_registrations', 
               'export_as_csv', 'retry_ctfd_sync_from_csv']    

    def approve_registrations(self, request, queryset):
        queryset.update(is_approved=True)
        self.message_user(request, "Selected registrations have been approved.")
    approve_registrations.short_description = "Approve selected registrations"

    def reject_registrations(self, request, queryset):
        queryset.update(is_approved=False)
        self.message_user(request, "Selected registrations have been rejected.")
    reject_registrations.short_description = "Reject selected registrations"

    def reject_all_registrations(self, request, queryset):
        SpecialPassRegistration.objects.update(is_approved=False)
        self.message_user(request, "All registrations have been rejected.")
    reject_all_registrations.short_description = "Reject all registrations"

    def export_as_csv(self, request, queryset):
        import csv
        from django.http import HttpResponse

        field_names = [field.name for field in SpecialPassRegistration._meta.fields]

        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="special_pass_registrations.csv"'

        writer = csv.writer(response)
        writer.writerow(field_names)

        for obj in queryset:
            row = [getattr(obj, field) for field in field_names]
            writer.writerow(row)

        return response
    export_as_csv.short_description = "Export Selected as CSV"

@admin.register(BasicPassRegistration)
class BasicPassAdmin(admin.ModelAdmin):
    list_display = ('firstname', 'lastname', 'discord_id', 'date_joined','school','year','student_id')
    list_filter = ['school', 'date_joined']
    search_fields = ('firstname', 'lastname')

