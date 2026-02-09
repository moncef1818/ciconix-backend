from django.shortcuts import render
from teams.models import Team
from .models import Token , TokenSubmission
from .serializers import TokenSubmitSerializer, TokenSubmissionSerializer, TeamTokenHistorySerializer, TeamTokenStatsSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.contrib.auth.hashers import check_password ,make_password
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.db.models import Sum


class TokenSubmitView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TokenSubmitSerializer(data=request.data)
        if serializer.is_valid():
            raw_token = serializer.validated_data['token']
            token = None

            for t in Token.objects.all():
                if t.check_token(raw_token):
                    token = t
                    break
            
            if token is None:
                return Response({
                    "success": False,
                    "message": "Invalid token"
                }, status=status.HTTP_400_BAD_REQUEST)
            

            team = request.user
            if TokenSubmission.objects.filter(team=team, token=token).exists():
                return Response({
                    "success": False,
                    "message": "Token already submitted by this team"
                }, status=status.HTTP_400_BAD_REQUEST)
            
            submission = TokenSubmission.objects.create(team=team, token=token)

            return Response({
                "success": True,
                "message": "Token submitted successfully",
                "data": TokenSubmissionSerializer(submission).data
            }, status=status.HTTP_201_CREATED)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class TeamTokenHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        team = request.user
        submission = TokenSubmission.objects.filter(team=team)

        stats = {
            "total_tokens": submission.count(),
            "total_points": submission.aggregate(total=Sum('token__base_points')).get('total') or 0
        }
        serializer = TeamTokenHistorySerializer(submission, many=True)
        return Response({
            "success": True,
            "data": serializer.data,
            "stats": stats
        },status=status.HTTP_200_OK)