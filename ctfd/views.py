from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny , IsAuthenticated
from django.conf import settings

class CTFdConfigView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ctfd_url = settings.CTFD_URL
        return Response({
            "success": True,
            "data": {
                "ctfd_url": ctfd_url
            }
        }, status=status.HTTP_200_OK)

# Create your views here.
