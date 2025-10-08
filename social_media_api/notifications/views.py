from django.shortcuts import render
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from .models import Notification
from .serializers import NotificationSerializer
from django.contrib.contenttypes.models import ContentType
from django.shortcuts import get_object_or_404

# Create your views here.



# View for fetching notifications
#Returns all notifications for a user, Orders by newest first; includes unread/read
class NotificationListView(generics.ListAPIView):  
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Notification.objects.filter(recipient=self.request.user).order_by('-timestamp')





# Helper function to create a notification
#Helper to make notifications from any app
#Used when someone likes, comments, or follow
#def create_notification(recipient, actor, verb, target=None):
    #if recipient != actor:  # avoid self-notifications
     #   Notification.objects.create(
      #      recipient=recipient,
       #     actor=actor,
        #    verb=verb,
         #   target=target)


    
# View to mark notifications as read
#Marks a single notification as read
#Helps users clear unread badges
#class MarkAsReadView(generics.UpdateAPIView):
    #serializer_class = NotificationSerializer
    #permission_classes = [permissions.IsAuthenticated]

    #def put(self, request, pk):
        #notification = get_object_or_404(Notification, pk=pk, recipient=request.user)
        #notification.is_read = True
       # notification.save()
        #return Response({'message': 'Notification marked as read'}, status=status.HTTP_200_OK)
    

