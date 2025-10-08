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
from django.shortcuts import get_object_or_404
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

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, _ = Token.objects.get_or_create(user=user)
        return Response({
            'user': CustomUserSerializer(user).data,
            'token': token.key
        }, status=status.HTTP_200_OK)

    
    def get_object(self):
        return self.request.user
    

class FollowUserView(generics.GenericAPIView):
    permission_classes = [ permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, user_id):
        #Fetches the user to be followed by user_id from the URL.If no such user exists, Django automatically raises a 404 response
        user_to_follow = get_object_or_404(CustomUser, id=user_id) 

        #Adds the target user to the current user’s “following” list, which is a ManyToManyField relation defined in my CustomUser model
        if user_to_follow == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        else:
            request.user.following.add(user_to_follow)
            return Response({"message": f"You are now following {user_to_follow.username}"}, status=status.HTTP_200_OK)
        

class UnfollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer

    def post(self, request, user_id):
        user_to_unfollow = get_object_or_404(CustomUser, id=user_id)
        if user_to_unfollow == request.user:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        
        else:
            request.user.following.remove(user_to_unfollow)
            return Response({"message": f"You Unfollowed {user_to_unfollow.username}"}, status=status.HTTP_200_OK)