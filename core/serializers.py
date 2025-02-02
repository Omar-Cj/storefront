from djoser.serializers import UserCreateSerializer as BaseUserCreateSerializer, UserSerializer as BaseUserSerializer
from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from .models import User

class UserCreateSerializer(BaseUserCreateSerializer):
    class Meta(BaseUserCreateSerializer.Meta):
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name']



class UserSerializer(BaseUserSerializer):
    id = serializers.IntegerField(read_only=True)
    class Meta(BaseUserSerializer.Meta):
        fields = ['id','username', 'email','first_name', 'last_name', 'last_login']




