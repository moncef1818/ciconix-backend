from django.contrib import admin
from .models import SpecialPassRegistration, BasicPassRegistration
from teams.models import Team

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
        """FORCE team creation on approval"""
        was_approved = obj.is_approved
        super().save_model(request, obj, form, change)
        
        if obj.is_approved and not Team.objects.filter(registration=obj).exists():
            # ✅ Generate SECURE random password
            secure_password = Team.generate_secure_password()
            
            # ✅ Create team as proper Django User
            team = Team.objects.create_user(
                email=obj.email1,
                team_name=obj.team_name,
                password=secure_password  # ✅ Auto-hashed
            )
            
            # ✅ Link registration
            team.registration = obj
            team.save()
            
            # ✅ Sync to CTFd
            ctfd_id = team.sync_to_ctfd(secure_password)
            
            # ✅ Success message with password (you can email this later)
            message = f"✅ Team '{team.team_name}' created!\n🔑 Password: `{secure_password}`\n🌐 CTFd ID: {ctfd_id or 'Pending'}"
            self.message_user(request, message, level='success')
            
        elif not obj.is_approved and was_approved:
            self.message_user(request, "Team unapproved")
    

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

