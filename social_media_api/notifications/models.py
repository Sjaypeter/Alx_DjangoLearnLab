from django.db import models
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

User = settings.AUTH_USER_MODEL


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications')
    verb = models.CharField(max_length=200)
    ## Generic relationship for any model, it allows linking for more than one model unlike Foreignkey (e.g. Post, Comment)
    target_content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True) #stores information about all models in my project
    target_object_id = models.PositiveBigIntegerField(null=True, blank=True) #This stores the primary key (ID) of the target object.
    target = GenericForeignKey("target_content_type", "target_object_id") #combines the two fields above (content_type + object_id) into a single easy-to-use field

    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.actor} {self.verb} {self.target} → {self.recipient}"
