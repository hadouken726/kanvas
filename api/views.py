import re
from rest_framework.views import APIView
from api.serializers import (
    UserSerializer,
    LoginSerializer,
    CourseSerializer,
    RegistrationInCourseReadSerializer,
    RegistrationInCourseWriteSerializer
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from api.models import Course
from django.shortcuts import get_object_or_404

class AccViews(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        user_to_post = User.objects.get_or_create(**serializer.validated_data)
        print(user_to_post)
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

class CourseView(APIView):
    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = Course.objects.get_or_create(**serializer.validated_data)[0]
        return Response(data=CourseSerializer(course).data, status=status.HTTP_201_CREATED)
    

    def put(self, request, course_id):
        try:
            Course.objects.get(id=course_id)
        except:
            return Response(data={"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RegistrationInCourseWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users_list = serializer.validated_data['users_ids']
        try:
            fetch_list = [User.objects.get(id=user_id) for user_id in users_list]
        except:
            return Response(data={'errors': 'invalid user_id list'}, status=status.HTTP_404_NOT_FOUND)
        unrepeated_fetch_list = list(set(fetch_list))
        getted_course.users.set(unrepeated_fetch_list)
        return Response(data=RegistrationInCourseReadSerializer(instance=getted_course).data, status=status.HTTP_200_OK)
        