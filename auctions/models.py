from django.contrib.auth.models import AbstractUser
from django.db import models

CATEGORIES= [
    ('TECH', 'Technologies'),
    ('TOYS', 'Toys'),
    ('HOME', 'Home')
]

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length=254)
    price = models.FloatField()
    image = models.CharField(max_length=500)
    category = models.CharField(max_length=3)
    date = models.CharField(max_length=64)



