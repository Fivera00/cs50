from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class User(AbstractUser):
    pass

class Games(models.Model):
    name = models.CharField(max_length=100)
    isDefault = models.BooleanField(default=False)
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'isDefault': self.isDefault
        }
        
class Categories(models.Model):
    categoryName = models.CharField(max_length=100)
    def serialize(self):
        return {
            'id': self.id,
            'categoryName': self.categoryName
        }

class Challenge(models.Model):
    titleChallenge = models.CharField(max_length=500)
    imageChallenge = models.CharField(max_length=500, blank=True)
    isChallenge = models.BooleanField(default=False)

    categoryChallenge = models.ForeignKey(Categories, on_delete=models.CASCADE)
    gameChallenge = models.ForeignKey(Games, on_delete=models.CASCADE)
    
    def serialize(self):
        return {
            'id': self.id,
            'titleChallenge': self.titleChallenge,
            'imageChallenge': self.imageChallenge,
            'isChallenge': self.isChallenge,
            'categoryChallenge': self.categoryChallenge.serialize(),
            'gameChallenge': self.gameChallenge.serialize()
        }

