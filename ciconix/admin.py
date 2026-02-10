# Create new file: ciconix/admin_dashboard.py

from django.contrib import admin
from django.urls import path
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from teams.models import Team
from registration.models import SpecialPassRegistration, BasicPassRegistration
from hackathon.models import Project
from tokens.models import Token, TokenSubmission

class DashboardAdmin(admin.AdminSite):
    site_header = "CICONIX Admin Dashboard"
    site_title = "CICONIX Admin"
    index_title = "Event Overview"
    
    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path('dashboard/', self.admin_view(self.dashboard_view), name='dashboard'),
        ]
        return custom_urls + urls
    
    @staff_member_required
    def dashboard_view(self, request):
        context = {
            **self.each_context(request),
            'total_registrations': SpecialPassRegistration.objects.count(),
            'approved_teams': Team.objects.filter(is_active=True).count(),
            'pending_approvals': SpecialPassRegistration.objects.filter(is_approved=False).count(),
            'projects_submitted': Project.objects.count(),
            'total_tokens': Token.objects.count(),
            'token_submissions': TokenSubmission.objects.count(),
            'basic_registrations': BasicPassRegistration.objects.count(),
        }
        return render(request, 'admin/dashboard.html', context)

# Use this in urls.py instead of default admin
# admin_site = DashboardAdmin(name='admin')