from rest_framework import serializers
from .models import Team
from django.contrib.auth import authenticate

class TeamSerializer(serializers.ModelSerializer):
    team_name = serializers.CharField()
    password = serializers.CharField(write_only=True)

    class Meta:  # ✅ Add this
        model = Team
        fields = ['team_name', 'password']

    def validate(self,data):
        team_name = data.get('team_name')
        password = data.get('password')

        if team_name and password:
            try:
                team = Team.objects.get(team_name=team_name)
            except Team.DoesNotExist:
                raise serializers.ValidationError('Invalid team name or password')
            
            if not team.check_password(password):
                raise serializers.ValidationError('Invalid team name or password')
            if not team.is_active:
                raise serializers.ValidationError('Team account is disabled')
            
            data['user'] = team
        else:
            raise serializers.ValidationError('Must include team name and password')
        return data