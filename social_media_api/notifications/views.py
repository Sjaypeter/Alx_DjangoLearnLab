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
