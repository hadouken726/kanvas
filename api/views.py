import re
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from api.serializers import (
    UserSerializer,
    UserInCourseSerializer,
    LoginSerializer,
    CourseSerializer,
    RegistrationInCourseReadSerializer,
    RegistrationInCourseWriteSerializer,
    ActivitySerializer,
    SubmissionReadSerializer,
    SubmissionGradeSerializer
)
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework import serializers, status
from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from django.contrib.auth.hashers import make_password
from api.models import Activity, Course, Submission
from django.shortcuts import get_object_or_404
from rest_framework.authentication import TokenAuthentication
from api.permissions import IsInstructor, ReadOnlyCourses, IsFacilitator, IsStudent


class AccViews(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        serializer.validated_data['password'] = make_password(serializer.validated_data['password'])
        try:
            getted_user = User.objects.get(username=serializer.validated_data['username'])
            return Response({'msg': 'user already exists!'}, status=status.HTTP_409_CONFLICT)
        except User.DoesNotExist:
            user_to_post = User.objects.create(**serializer.validated_data)
        user = UserSerializer(user_to_post)
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
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor | ReadOnlyCourses]


    def post(self, request):
        serializer = CourseSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        course = Course.objects.get_or_create(**serializer.validated_data)[0]
        return Response(data=CourseSerializer(course).data, status=status.HTTP_201_CREATED)
    

    def put(self, request, course_id):
        try:
            getted_course = Course.objects.get(id=course_id)
        except Course.DoesNotExist:
            return Response(data={"errors": "invalid course_id"}, status=status.HTTP_404_NOT_FOUND)
        serializer = RegistrationInCourseWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        users_list = serializer.validated_data['user_ids']
        try:
            fetch_list = [User.objects.get(id=user_id) for user_id in users_list]
        except:
            return Response(data={'errors': 'invalid user_id list'}, status=status.HTTP_404_NOT_FOUND)
        unrepeated_fetch_list = list(set(fetch_list))
        if any(user.is_staff or user.is_superuser for user in unrepeated_fetch_list):
            return Response({'errors': 'Only students can be enrolled in the course.'}, status=status.HTTP_400_BAD_REQUEST)
        getted_course.users.set(unrepeated_fetch_list)
        updated_course = RegistrationInCourseReadSerializer(instance=getted_course)
        return Response(data=updated_course.data, status=status.HTTP_200_OK)
    

    def get(self, request, course_id=None):
        if course_id:
            try:
                course = Course.objects.get(id=course_id)
            except Course.DoesNotExist:
                return Response(data={'errors': 'invalid course_id'}, status=status.HTTP_404_NOT_FOUND)
            course = RegistrationInCourseReadSerializer(instance=course)
            return Response(data=course.data, status=status.HTTP_200_OK)
        courses = Course.objects.all()
        courses = RegistrationInCourseReadSerializer(instance=courses, many=True)
        return Response(data=courses.data, status=status.HTTP_200_OK)
    

    def delete(self, request, course_id):
        course_to_delete = get_object_or_404(Course, id=course_id)
        course_to_delete.delete()
        return Response(data='', status=status.HTTP_204_NO_CONTENT)

    
class ActivityView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsInstructor | IsFacilitator]


    def post(self, request):
        serializer = ActivitySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        try:
            activity_to_post = Activity.objects.get(title=serializer.validated_data['title'])
            activity_to_post.points = serializer.validated_data['points']
            activity_to_post.save()
        except Activity.DoesNotExist:
            activity_to_post = Activity.objects.create(**serializer.validated_data)
        activity_to_post = ActivitySerializer(instance=activity_to_post)
        return Response(data=activity_to_post.data, status=status.HTTP_201_CREATED)
    

    def get(self, request):
        activities = Activity.objects.all()
        activities = ActivitySerializer(instance=activities, many=True)
        return Response(data=activities.data, status=status.HTTP_200_OK)


class SubmissionView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [(IsInstructor | IsFacilitator | IsStudent) & IsAuthenticated]


    def post(self, request, activity_id):
        activity = get_object_or_404(Activity, id=activity_id)
        submission_serializer = SubmissionReadSerializer(data=request.data)
        submission_serializer.is_valid(raise_exception=True)
        submission = Submission.objects.create(user=request.user, activity=activity, **submission_serializer.validated_data)
        submission = SubmissionReadSerializer(instance=submission)
        return Response(data=submission.data, status=status.HTTP_201_CREATED)
    

    def put(self, request, submission_id):
        submission = get_object_or_404(Submission, id=submission_id)
        serializer = SubmissionGradeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        submission.grade = serializer.validated_data['grade']
        submission.save()
        submission = SubmissionGradeSerializer(instance=submission)
        return Response(data=submission.data, status=status.HTTP_200_OK)
    

    def get(self, request):
        submissions = Submission.objects.all()
        if not request.user.is_staff and not request.user.is_superuser:
            submissions = Submission.objects.filter(user_id=request.user.id)
        submissions = SubmissionReadSerializer(instance=submissions, many=True)
        return Response(data=submissions.data, status=status.HTTP_200_OK)


