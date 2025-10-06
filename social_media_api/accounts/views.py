from django.shortcuts import render,redirect
from . serializers import CustomUserSerializer, RegisterSerializer, LoginSerializer
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.authtoken.models import Token
from .models import CustomUser
# Create your views here.


User = get_user_model()


class RegisterView(generics.CreateAPIView):
    queryset = CustomUser.objects.all()
    serializer_class = RegisterSerializer
    

    def create(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        user = User.objects.get(username=response.data['username'])
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': CustomUserSerializer(user).data,
            "token": token.key
        }, status=status.HTTP_201_CREATED)
    

class LoginView(APIView):

    def post(self, request, *args, **kwargs):
        response = super().create(request, *args, **kwargs)
        token =  Token.objects.get(key=response.data['token'])
        return Response({
            'user': CustomUserSerializer(token.user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)
    
    def get_object(self):
        return self.request.user
    