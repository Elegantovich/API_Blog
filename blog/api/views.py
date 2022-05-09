from rest_framework import status, viewsets
from rest_framework.views import APIView
from .models import Post, User
from api.serializers import PostSerializer, AuthSerializer
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404


class PostViewSet(viewsets.ModelViewSet):
    serializer_class = PostSerializer
    queryset = Post.objects.all()
    lookup_field = 'pk'


def get_tokens_for_user(user):
    """
    Create token.
    """
    access = AccessToken.for_user(user)
    return {'access': str(access)}


class RecieveToken(APIView):
    """
    Recieve token for authorization.
    """
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        serializer = AuthSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST
            )
        user = get_object_or_404(User, username=username, password=password)
        response = {'auth_token': get_tokens_for_user(user)}
        return Response(response, status=status.HTTP_200_OK)