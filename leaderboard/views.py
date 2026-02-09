from django.shortcuts import render
from teams.models import Team
from ctfd.service import CTFdService
from hackathon.models import Project
from django.db.models import Sum
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated

class LeaderboardView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):

        ctf_scores = CTFdService.get_team_scores()
        teams = Team.objects.filter(is_active=True,is_staff=False)

        leaderboard = []
        for team in teams:
            ctf_points = ctf_scores.get(team.ctfd_team_id,0)
            
            try :
                project = Project.objects.get(team=team)
                project_points = project.total_score
            except Project.DoesNotExist:
                project_points = 0

            token_points = team.token_submissions.aggregate(total=Sum('token__base_points'))['total'] or 0

            total_points = ctf_points + project_points + token_points
            leaderboard.append({
                "team_name":team.team_name,
                "ctf_points": ctf_points,
                "project_points": project_points,
                "token_points": token_points,
                "total_points": total_points
            })


        leaderboard.sort(key=lambda x: x['total_points'], reverse=True)
        for idx, entry in enumerate(leaderboard,start=1):
            entry['rank'] = idx
        
        return Response({
            "success": True,
            "data": leaderboard
        }, status=status.HTTP_200_OK)

