from .models import Post, User, Blog
from rest_framework import serializers
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import check_password
from rest_framework import status
from rest_framework.response import Response


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'first_name', 'last_name')
        model = User


class BlogSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        fields = ('author', 'description')
        model = Blog


class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    blog = BlogSerializer(read_only=True)

    class Meta:
        exclude = ('date_create',)
        model = Post