from django.urls import path,include
from . views import PostViewSet,CommentViewSet , FeedView
from rest_framework.routers import DefaultRouter


router = DefaultRouter()

router.register(r'comments', CommentViewSet, basename='comment')
router.register(r'posts',PostViewSet, basename='posts')

urlpatterns = [
    path('', include(router.urls)),
    path('feed/', FeedView.as_view(), name='feed'),
]
