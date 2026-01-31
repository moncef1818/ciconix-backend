from django.shortcuts import render
from django.http import HttpResponse
from .models import SpecialPassRegistration, BasicPassRegistration
from .serializers import BasicPassRegistrationSerializer , SpecialPassRegistrationSerializer
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

class BasicPassRegistrationView(APIView):
    
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = BasicPassRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Success": True,
                "message": "Basic Pass Registration successful",
                "data": serializer.data},
                status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        
class SpecialPassRegistrationView(APIView):

    permission_classes = [AllowAny]

    def post(self, request):
        serializer = SpecialPassRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({
                "Success": True,
                "message": "Special Pass Registration successful",
                "data": serializer.data},
                status=status.HTTP_201_CREATED)
        return Response({"errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)


# Create your views here.
