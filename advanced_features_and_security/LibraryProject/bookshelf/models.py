from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.backends import BaseUserManager
from django.contrib.auth.models import Permission
# Create your models here.

class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    publication_year = models.IntegerField()
    
    class Meta:
        Permission = [
            ("can_create", "Can create book"),
            ("can_delete", "Can delete book"),
            ("can_edit", "Can edit book"),
            ("can_view", "Can view book")
        ]
    
    def __str__(self):
        return self.title



class CustomUser(AbstractUser):
    date_of_birth = models.DateField(null=True,blank=True)
    profile_photo = models.ImageField(null=True,blank=True)
    
    
class CustomUserManager(BaseUserManager):
    def create_user(self,request,username=None,password=None):
        pass
    
        
    def create_superuser(self,request,username=None,password=None):
        pass
