from django.db.models.fields import IntegerField
from rest_framework import serializers
from django.contrib.auth.models import User


class UserSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    is_superuser = serializers.BooleanField()
    is_staff = serializers.BooleanField()


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(write_only=True)
    password = serializers.CharField(write_only=True)


class CourseSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = UserSerializer(many=True, read_only=True)


class RegistrationInCourseWriteSerializer(serializers.Serializer):
    users_ids = serializers.ListField(child=serializers.IntegerField(), write_only=True)


class RegistrationInCourseReadSerializer(serializers.Serializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField()
    users = UserSerializer(serializers.ListField(child=UserSerializer()), read_only=True, many=True)