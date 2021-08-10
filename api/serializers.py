from django.db.models.fields import IntegerField
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()


class UserInCourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = UserSerializer(many=True, read_only=True)


class RegistrationInCourseWriteSerializer(serializers.Serializer):
    user_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)


class RegistrationInCourseReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = UserInCourseSerializer(many=True)


class SubmissionReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    grade = serializers.IntegerField(read_only=True)
    repo = serializers.CharField()
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(read_only=True)


class ActivitySerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    title = serializers.CharField()
    points = serializers.IntegerField()
    submissions = SubmissionReadSerializer(many=True, read_only=True)


class SubmissionGradeSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    grade = serializers.IntegerField()
    repo = serializers.CharField(read_only=True)
    user_id = serializers.PrimaryKeyRelatedField(read_only=True)
    activity_id = serializers.PrimaryKeyRelatedField(read_only=True)