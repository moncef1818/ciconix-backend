# flags/serializers.py

from rest_framework import serializers
from .models import Token, TokenSubmission
import re

class TokenSubmitSerializer(serializers.Serializer):
    token = serializers.CharField(max_length=200)
    
    def validate_token(self, value):  
        
        if not re.match(r'^CIC\{.+\}$', value):
            raise serializers.ValidationError(
                "Invalid token format. Must start with CIC{ and end with }"
            )
        
        if len(value) < 32:
            raise serializers.ValidationError(
                "Token is too short"
            )
        
        return value


class TokenSubmissionSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField(source='team.team_name', read_only=True)
    points = serializers.IntegerField(source='token.base_points', read_only=True)
    submitted_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = TokenSubmission
        fields = ['id', 'team_name', 'points', 'submitted_at']
        read_only_fields = ['id', 'team_name', 'points', 'submitted_at']


class TeamTokenHistorySerializer(serializers.ModelSerializer):
    """For showing a team's token submission history"""
    points = serializers.IntegerField(source='token.base_points', read_only=True)
    submitted_at = serializers.DateTimeField(read_only=True)
    
    class Meta:
        model = TokenSubmission
        fields = ['id', 'points', 'submitted_at']
        read_only_fields = fields


class TeamTokenStatsSerializer(serializers.Serializer):
    """For showing team's total points from tokens"""
    total_tokens = serializers.IntegerField()
    total_points = serializers.IntegerField()
    submissions = TeamTokenHistorySerializer(many=True)