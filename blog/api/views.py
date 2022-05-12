from datetime import datetime

from api.serializers import BlogSerializer, FollowsSerializer, PostSerializer
from blog.sent_mail import send_message_to_mail
from django.contrib.auth.hashers import check_password
from rest_framework import mixins, status, viewsets
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken

from .constant import MESSAGE
from .models import Blog, Date, Follow, Post, Read, User
from .pagination import CustomPagination
from .permissions import AuthorOrAdminOrReadonly


now = datetime.now().strftime("%Y-%m-%d")


class PostViewSet(viewsets.ModelViewSet):
    """
    ViewSet for Post model.
    """
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        blog = get_object_or_404(Blog, id=self.kwargs.get('blog_id'))
        return blog.posts.all()

    def perform_create(self, serializer):
        obj = Date.objects.filter(date=now).exists()
        blog = Blog.objects.get(author=self.request.user)
        serializer.save(blog=blog)
        if not obj:
            if Post.objects.count() < 5:
                pass
            else:
                last_post = Post.objects.order_by("-id")[0:5]
                all_users = User.objects.all()
                for user in all_users:
                    send_message_to_mail('defaul@ru.ru', user.username,
                                         last_post)
                Date.objects.create()

    def perform_update(self, serializer):
        blog = Blog.objects.get(author=self.request.user)
        id = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=id)
        if blog.id != post.blog.id:
            print(blog.id, post.blog.id)
            return Response({'response': 'Error!'},
                            status=status.HTTP_400_BAD_REQUEST)
        serializer.save(blog=blog)

    def perform_destroy(self, instance):
        blog = Blog.objects.get(author=self.request.user)
        id = self.kwargs.get('pk')
        post = get_object_or_404(Post, id=id)
        if blog.id != post.blog.id:
            print(blog.id, post.blog.id)
            return Response({'response': 'Error!'},
                            status=status.HTTP_400_BAD_REQUEST)
        instance.delete()


class ListRetrieveUpdateViewSet(mixins.ListModelMixin,
                                mixins.RetrieveModelMixin,
                                mixins.UpdateModelMixin,
                                viewsets.GenericViewSet):
    pass


class BlogViewSet(ListRetrieveUpdateViewSet):
    """
    Get info by all blogs and update your blog.
    """
    serializer_class = BlogSerializer
    permission_classes = (AuthorOrAdminOrReadonly,)
    queryset = Blog.objects.all()
    lookup_field = 'pk'


class NewsView(APIView, CustomPagination):
    """
    Get favorite posts.
    """
    def get(self, request):
        blogs = Blog.objects.filter(following__user=request.user)
        posts_list = []
        for i in blogs:
            posts = i.posts.all()
            for item in posts:
                post = get_object_or_404(Post, id=item.id)
                read_obj = Read.objects.filter(user=request.user,
                                               post=post).exists()
                if read_obj:
                    post.is_read = True
                    post.save()
                else:
                    post.is_read = False
                    post.save()
                posts_list.append(post)
        results = self.paginate_queryset(posts_list, request, view=self)
        serializer = PostSerializer(results, many=True)

        return self.get_paginated_response(serializer.data)


def get_tokens_for_user(user):
    """
    Create token.
    """
    access = AccessToken.for_user(user)
    return {'access': str(access)}


class RecieveToken(APIView):
    """
    Recieve token for authorization and create blog.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data['username']
            password = request.data['password']
        except KeyError:
            response = {'response': MESSAGE}
            return Response(response, status=status.HTTP_404_NOT_FOUND)
        user = get_object_or_404(User, username=username)
        blog_is = Blog.objects.filter(author=user.id).exists()
        if not blog_is:
            Blog.objects.create(author=user)
        pass_encrypted_valid = check_password(password, user.password)
        if not pass_encrypted_valid:
            if password != user.password:
                return Response({'response': 'Error! Passwords do not match!'},
                                status=status.HTTP_400_BAD_REQUEST)
        response = {'auth_token': get_tokens_for_user(user)}
        return Response(response, status=status.HTTP_200_OK)


class FollowView(APIView):
    """
    Subscribe and unsubscribe to blog.
    """
    def post(self, request, blog_id):
        user = request.user.username
        blog = get_object_or_404(Blog, id=blog_id)
        follow = {'user': request.user,
                  'blog': blog}
        if user == blog.author.username:
            return Response(
                {'response': 'You not can subscribe to yourself!'},
                status=status.HTTP_400_BAD_REQUEST)
        if Follow.objects.filter(user=request.user, blog=blog).exists():
            return Response(
                {'response': 'Follow also exist!'},
                status=status.HTTP_400_BAD_REQUEST)
        serializer = FollowsSerializer(follow)
        Follow.objects.create(user=request.user, blog=blog)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, blog_id):
        user = request.user
        blog = get_object_or_404(Blog, id=blog_id)
        follow = get_object_or_404(Follow, user=user, blog=blog)
        follow.delete()
        return Response({'response': 'Removed!'},
                        status=status.HTTP_204_NO_CONTENT)


class ReadView(NewsView):
    """
    Subscribe and unsubscribe to blog.
    """
    def post(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        read_exist = Read.objects.filter(user=user, post=post).exists()
        if not read_exist:
            Read.objects.create(user=request.user, post=post)
        serializer = PostSerializer(post)
        serializer_dict = serializer.data
        serializer_dict['is_read'] = True
        return Response(serializer_dict, status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        Read_obj = get_object_or_404(Read, user=user, post=post)
        Read_obj.delete()
        return Response({'response': 'Removed!'},
                        status=status.HTTP_204_NO_CONTENT)
