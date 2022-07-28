from django.urls import include, path
from rest_framework import routers

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, SignUpView, TitleViewSet, TokenView,
                    UserViewSet)

router = routers.DefaultRouter()

router.register('genres', GenreViewSet, basename='genre-list')
router.register('titles', TitleViewSet, basename='title-list')
router.register('categories', CategoryViewSet, basename='category-list')
router.register('users', UserViewSet)

router.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='review-list'
)

router.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentViewSet,
    basename='comment-list'
)


urlpatterns = [
    path(
        'v1/auth/signup/',
        SignUpView.as_view({'post': 'create'}),
        name='auth-signup'
    ),
    path(
        'v1/auth/token/',
        TokenView.as_view(),
        name='auth-token'
    ),
    path('v1/', include(router.urls)),
]
