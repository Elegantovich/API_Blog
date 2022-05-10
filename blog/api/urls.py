from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import (RecieveToken, PostViewSet, BlogViewSet, FollowView,
                    NewsView, ReadView)

router = DefaultRouter()
router.register('blogs', BlogViewSet)
router.register(r'blogs/(?P<blog_id>[\d+]+)/posts',
                PostViewSet,
                basename='posts'
                )

urlpatterns = [
    path('auth/token/login/', RecieveToken.as_view()),
    path('news/', NewsView.as_view()),
    path('news/<int:post_id>/read/', ReadView.as_view()),
    path('', include(router.urls)),
    path('blogs/<int:blog_id>/subscribe/',
         FollowView.as_view()),
]
