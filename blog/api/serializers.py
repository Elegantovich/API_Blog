from .models import Post, User
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'first_name', 'last_name')
        model = User


class BlogSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('description',)
        model = User


class PostSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)
    blog = BlogSerializer(read_only=True)

    class Meta:
        fields = '__all__'
        model = Post