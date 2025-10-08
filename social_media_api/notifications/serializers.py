from rest_framework import serializers
from . models import Notification

class NotificationSerializer(serializers.ModelSerializer):
    actor = serializers.StringRelatedField()
    recipient = serializers.StringRelatedField()
    target = serializers.SerializerMethodField() #Displays a readable name of the related object (like a Post title or Comment

    class Meta:
        model = Notification

        fields = [
            'id',
            'recipient_username',
            'actor_username',
            'verb',
            'target',
            'timestamp',
            'read'
        ]
