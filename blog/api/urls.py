from django.urls import include, path
from rest_framework.routers import DefaultRouter
from .views import RecieveToken, PostViewSet, BlogViewSet

router = DefaultRouter()
router.register('blogs',
                BlogViewSet
                )
router.register(r'blogs/(?P<blog_id>[\d+]+)/posts',
                PostViewSet,
                basename='posts'
                )

urlpatterns = [
    path('auth/token/login/', RecieveToken.as_view()),
    # path('news/', .as_view()),
    path('', include(router.urls))
]
