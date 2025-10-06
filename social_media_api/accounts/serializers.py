from rest_framework import serializers
from . models import CustomUser
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ["__all__"]

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only= True,min_length=8)

    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password']

    def create(self,validated_data):
        user = CustomUser.objects.create_user(
            username= validated_data['username'],
            email= validated_data['email'],
            password= validated_data['password']

        )
        Token.objects.create(user=user)
        return user
    
class LoginSerializer(serializers.ModelSerializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only= True,min_length=8)

    def validate(self,data):
        user = authenticate(username=data['username'], password=data['password'])
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        data['user'] = user
        return data


