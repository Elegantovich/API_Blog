from rest_framework import status, viewsets, mixins
from rest_framework.views import APIView
from .models import Post, User, Blog
from api.serializers import PostSerializer, BlogSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from django.contrib.auth.hashers import check_password
from .permissions import AuthorOrAdminOrReadonly
from .constant import MESSAGE


class PostViewSet(viewsets.ModelViewSet):
    permission_classes = (AuthorOrAdminOrReadonly,)
    serializer_class = PostSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        blog = get_object_or_404(Blog, id=self.kwargs.get('blog_id'))
        return blog.posts.all()

    def perform_create(self, serializer):
        blog = Blog.objects.get(author=self.request.user)
        serializer.save(blog=blog)

class ListRetrieveViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin,
                          mixins.UpdateModelMixin, viewsets.GenericViewSet):
    pass


class BlogViewSet(ListRetrieveViewSet):
    permission_classes = (AuthorOrAdminOrReadonly,)
    serializer_class = BlogSerializer
    queryset = Blog.objects.all()
    lookup_field = 'pk'


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
                                status=status.HTTP_400_BAD_REQUEST
            )
        response = {'auth_token': get_tokens_for_user(user)}
        return Response(response, status=status.HTTP_200_OK)

