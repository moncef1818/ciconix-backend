# hackathon/serializers.py

from rest_framework import serializers
from .models import Project

class ProjectSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    
    class Meta:
        model = Project
        fields = ['id', 'team_name', 'project_link', 'submission_time', 'total_score']
        read_only_fields = ['id', 'team_name', 'submission_time', 'total_score']


class ProjectSubmitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        fields = ['project_link']
    
    def validate_project_link(self, value):
        """Ensure the URL is valid"""
        if not value.startswith(('http://', 'https://')):
            raise serializers.ValidationError("URL must start with http:// or https://")
        return value