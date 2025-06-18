from django.db import models
from lobby.models import User

# Create your models here.
class UserInfo(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profession = models.CharField(max_length=40)
    age = models.IntegerField()
    hobby = models.CharField(max_length=40)
    item = models.CharField(max_length=40)
    fact = models.CharField(max_length=100)
    health = models.CharField(max_length=100)
