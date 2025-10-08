from django.shortcuts import render
from rest_framework import generics
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from . permissions import IsAuthorOrReadOnly
from . models import Post, Comment
from . serializers import PostSerializer, CommentSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied

# Create your views here.

class PostViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['title', 'content']  # allow ?search=keyword
    ordering_fields = ['created_at', 'updated_at']
    ordering = ['-created_at']  # newest first

    #Automatically sets author to the logged-in user
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)



class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsAuthorOrReadOnly]


    def get_queryset(self):
          """
        Optionally filter comments by a specific post (if ?post_id= is passed).
        """
          queryset = Comment.objects.all()
          post_id = self.request.query_params.get('post_id')

          if post_id:
              queryset = queryset.filter(post_id=post_id)
              return queryset
          
    #Automatically sets author to the logged-in user
    def perform_create(self, serializer):
        post_id = self.request.data.get('post')
        if not post_id:
            raise PermissionDenied("A 'post' ID must be provided to create a comment")
        serializer.save(author=self.request.user, post_id=post_id)


class FeedView(generics.ListAPIView):
        serializer_class = PostSerializer
        permission_classes = [IsAuthenticated]

        def get_queryset(self): #Instead of returning all posts, it filters only the ones relevant to the logged-in user
            user = self.request.user #Gets the currently authenticated user from the incoming request
            following_users = user.following.all()#Fetches all the users that the current user follows, based on My CustomUser model’s ManyToMany relationship
            #This filters the Post model to include only posts authored by users the current user follows
            return Post.objects.filter(author__in=following_users).order_by('-created_at')