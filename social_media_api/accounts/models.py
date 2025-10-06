from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='profile_pics/',blank=True, null=True)
    followers = models.ManyToManyField('self',symmetrical=False, related_name='following', blank=True)
    # symmetrical=False means A following B doesn't imply B follows A


    def __str__(self):
        # prefer full name if available, otherwise username
        full = self.get_full_name()
        return full if full else self.username
