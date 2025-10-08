from django.shortcuts import render
from rest_framework.response import Response
from rest_framework import generics, status, permissions
from rest_framework import viewsets, permissions, filters
from rest_framework.permissions import IsAuthenticated
from . permissions import IsAuthorOrReadOnly
from . models import Post, Comment, Like
from . serializers import PostSerializer, CommentSerializer, LikeSerializer
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from notifications.models import Notification

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
        permission_classes = [permissions.IsAuthenticated]

        def get_queryset(self): #Instead of returning all posts, it filters only the ones relevant to the logged-in user
            user = self.request.user #Gets the currently authenticated user from the incoming request
            following_users = user.following.all()#Fetches all the users that the current user follows, based on My CustomUser model’s ManyToMany relationship
            #This filters the Post model to include only posts authored by users the current user follows
            return Post.objects.filter(author__in=following_users).order_by('-created_at')
        

class LikePostView(generics.GenericAPIView):
     permission_classes = [permissions.IsAuthenticated]
     serializer_class = LikeSerializer

     def post(self,request,pk): #Defines the POST handler. pk should match a path parameter my URL
          post = generics.get_object_or_404(Post, pk=pk) #Fetches the Post instance or returns a 404 if it doesn’t exist.
          like,created = Like.objects.get_or_create(user=request.user, post=post) #Tries to find an existing Like for this (user, post) pair; if none exists, it creates one.

          if not created:
               return Response({"error": "You already liked this post"}, status=status.HTTP_400_BAD_REQUEST)
          
          #CREATE NOTIFICATION
          if post.author != request.user: #Avoids creating a notification if the author liked their own post
               #creates notification record of the parameters below it
               Notification.objects.create(
                    recipient = post.author,
                    actor = request.user,
                    verb= "Liked your post",
                    target = post
               )
               return Response({"message": "Post liked successfully!"}, status=status.HTTP_201_CREATED)
          
class UnlikePostView(generics.GenericAPIView):
     permission_classes = [permissions.IsAuthenticated]

     def post(self,request, pk):
          post = generics.get_object_or_404(Post, pk=pk)
          like = Like.objects.filter(user=request.user, post=post).first()

          if like:
               like.delete()
               return Response({"message": "Post unliked successfully!"}, status=status.HTTP_200_OK)
          else:
            return Response({"error": "You have not liked this post."}, status=status.HTTP_400_BAD_REQUEST)