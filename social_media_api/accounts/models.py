from django.db import models
from django.contrib.auth.models import AbstractBaseUser

class CustomUser(AbstractBaseUser):
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='images/')
    followers = models.ManyToManyField('self', symmetrical=False, related_name="follower", blank= True)

    def __str__(self):
        return self.username
    
