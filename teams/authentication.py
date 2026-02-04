from .models import Team
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken

class TeamJWTAuthentication(JWTAuthentication):
    def get_user(self, validated_token):
        try:
            team_id = validated_token['team_id']
        except KeyError:
            raise InvalidToken('Token contained no team identification')

        try:
            team = Team.objects.get(id=team_id)
        except Team.DoesNotExist:
            raise InvalidToken('Team not found')

        return team
    
    
