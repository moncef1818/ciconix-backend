from django.shortcuts import render
from .models import Team
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import TeamSerializer
from ctfd.service import CTFdService
from hackathon.models import Project
from django.db.models import Sum



class TeamLoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TeamSerializer(data=request.data)
        
        # 1. Validate input (checks team existence & password)
        if serializer.is_valid():
            team = serializer.validated_data['user']
            
            # 2. Generate JWT tokens manually
            refresh = RefreshToken.for_user(team)
            
            # 3. Add custom claims if needed (optional)
            refresh['team_name'] = team.team_name

            return Response({
                "success": True,
                "message": "Login successful",
                "data": {
                    "team_name": team.team_name,
                    "ctfd_team_id": team.ctfd_team_id,
                    "access": str(refresh.access_token),   # should be stored in the frontend for authenticated requests
                    "refresh": str(refresh)                # stored in the front end can be used to get new access tokens when the old one expires
                }
            }, status=status.HTTP_200_OK)
            
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class TeamProfileView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        team = request.user
        team__ctfd_score = CTFdService.get_team_score(team.ctfd_team_id)
        
        try :
            project = Project.objects.get(team=team)
            team__project_score = project.total_score
        except Project.DoesNotExist:
            team__project_score = 0

        team__token_score = team.token_submissions.aggregate(total=Sum('token__base_points'))['total'] or 0

        team__total_score = team__ctfd_score + team__project_score + team__token_score

        return Response({
            "success": True,
            "data":{
                "team_name": team.team_name,
                "ctfd_team_id": team.ctfd_team_id,
                "email": team.email,
                "created_at": team.created_at,
                "ctfd_score": team__ctfd_score,
                "project_score": team__project_score,
                "token_score": team__token_score,
                "total_score": team__total_score
            }
        }, status=status.HTTP_200_OK)
    
class TeamLogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            # Blacklist the refresh token
            refresh_token = request.data.get("refresh")
            token = RefreshToken(refresh_token)
            token.blacklist()

            return Response({
                "success": True,
                "message": "Logout successful"
                  }, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({
                "success": False, 
                "message": str(e)}
                , status=status.HTTP_400_BAD_REQUEST)
