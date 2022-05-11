from rest_framework import serializers

from .models import Blog, Follow, Post, User


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('username', 'first_name', 'last_name')
        model = User


class BlogSerializer(serializers.ModelSerializer):

    author = UserSerializer(read_only=True)

    class Meta:
        fields = ('id', 'author', 'description')
        model = Blog


class PostSerializer(serializers.ModelSerializer):

    blog = BlogSerializer(read_only=True)

    class Meta:
        exclude = ('date_create',)
        model = Post


class FollowsSerializer(serializers.ModelSerializer):

    user = UserSerializer(read_only=True)
    blog = BlogSerializer()

    class Meta:
        model = Follow
        fields = ('user', 'blog')
