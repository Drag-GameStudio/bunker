from django.db import models


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=100, default="waiting")

    def __str__(self):
        return str(self.id)

class User(models.Model):
    

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    isOwner = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
