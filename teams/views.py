from django.shortcuts import render
from .models import Team
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth.hashers import check_password

class TeamLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        team_name = request.data.get('team_name')
        password = request.data.get('password')

        try:
            team = Team.objects.get(team_name=team_name)
            if check_password(password, team.password_hash):
                return Response({
                    "Success": True,
                    "message": "Login successful",
                    "data": {
                        "team_name": team.team_name,
                        "ctfd_team_id": team.ctfd_team_id
                    }},
                    status=status.HTTP_200_OK)
            else:
                return Response({"errors": "Invalid password"}, status=status.HTTP_401_UNAUTHORIZED)
        except Team.DoesNotExist:
            return Response({"errors": "Team does not exist"}, status=status.HTTP_404_NOT_FOUND)
# Create your views here.
