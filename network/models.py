from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.base import Model


class User(AbstractUser):
    pass

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.Case)
    followers = models.ManyToManyField(User, related_name="get_follower")

    def __str__ (self):  
        return f"{self.id}: {self.user.username} has {self.followers.count()} followers and follows {self.user.get_follower.count()} users"

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=500)
    date = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(User, related_name="get_likes_post")
    
    def __str__(self):
        return(f"{self.id}: {self.content} made by {self.user} on {self.date} has {self.likes.count()} likes")

