import re
from rest_framework.views import APIView
from api.serializers import UserSerializer, LoginSerializer
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password

class AccViews(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        user_to_post = User.objects.get_or_create(**serializer.validated_data)
        if not user_to_post[1]:
            return Response({'msg': 'user already exists!'}, status=status.HTTP_409_CONFLICT)
        user = UserSerializer(user_to_post[0])
        return Response(user.data, status=status.HTTP_201_CREATED)

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)   
        user_to_authenticate = serializer.validated_data
        user = authenticate(request=request, **user_to_authenticate)
        if user:
            token, _ = Token.objects.get_or_create(user=user)
            return Response({'token': str(token)}, status=status.HTTP_200_OK)
        return Response({'msg':'invalid user'}, status=status.HTTP_401_UNAUTHORIZED)




        
