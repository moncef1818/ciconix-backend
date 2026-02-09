from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from .models import Project
from .serializers import ProjectSerializer, ProjectSubmitSerializer


class ProjectSubmitView(APIView):
    """Submit or update project link"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        team = request.user
        
        # Check if project already exists for this team
        project = Project.objects.filter(team=team).first()
        
        if project:
            # Project already exists - update it
            serializer = ProjectSubmitSerializer(project, data=request.data, partial=True)
            action = "updated"
        else:
            # No project yet - create new one
            serializer = ProjectSubmitSerializer(data=request.data)
            action = "submitted"
        
        if serializer.is_valid():
            if project:
                # Update existing
                serializer.save()
            else:
                # Create new
                serializer.save(team=team)
            
            # Get the project to return full details
            project = Project.objects.get(team=team)
            
            return Response({
                "success": True,
                "message": f"Project {action} successfully",
                "data": ProjectSerializer(project).data
            }, status=status.HTTP_200_OK)
        
        return Response({
            "success": False,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class ProjectDetailView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        team = request.user
        try:
            Project = Project.objects.get(team=team)
            serializer = ProjectSerializer(Project)
            return Response({
                "success": True,
                "data": serializer.data
            }, status=status.HTTP_200_OK)
        except Project.DoesNotExist:
            return Response({
                "success": False,
                "message": "No project Submitted yet"
            }, status=status.HTTP_404_NOT_FOUND)
        
class AllProjectsView(APIView):

    persmission_classes = [IsAuthenticated]
    def get(self, request):
        projects = Project.objects-all()
        serializer = ProjectSerializer(projects, many=True)
        return Response({
            "success": True,
            "data": serializer.data
        }, status = status.HTTP_200_OK)
    