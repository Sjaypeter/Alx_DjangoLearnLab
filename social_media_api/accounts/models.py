from django.db import models
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    bio = models.TextField()
    profile_picture = models.ImageField(upload_to='images/')
    #Creates one-way following relationships (A can follow B without B following A)
    followers = models.ManyToManyField('self', symmetrical=False,related_name="following", blank= True) #symmetrical allows one-way following

    def __str__(self):
        return self.username
    
    def follow(self, user):
        """Follows another user"""
        if user != self:
            self.following.add(user)

    def unfollow(self, user):
        """Unfollows another user"""
        if user != self:
            self.following.remove(user)

    def is_following(self, user):
        """Checks if another user is following another"""

        return self.following.filter(id=user.id).exists()
    
    def is_followed_by(self,user):
        """Checks if another user follows this one"""
        return self.followers.filter(id=user.id).exists()
    


