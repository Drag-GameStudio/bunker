from django.db import models
from lobby.models import User

# Create your models here.
class UserInfo(models.Model):


    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    profession = models.CharField(max_length=40)
    profession_is_open = models.BooleanField(default=False)

    age = models.IntegerField()
    age_is_open = models.BooleanField(default=False)

    hobby = models.CharField(max_length=40)
    hobby_is_open = models.BooleanField(default=False)

    item = models.CharField(max_length=40)
    item_is_open = models.BooleanField(default=False)

    fact = models.CharField(max_length=100)
    fact_is_open = models.BooleanField(default=False)

    health = models.CharField(max_length=100)
    health_is_open = models.BooleanField(default=False)


    def get_data_in_json(self):
        user_data = {}
        lables = ["profession", "age", "hobby", "item", "fact", "health"]
        
        for lable in lables:
            user_data[lable] = {
                "value": getattr(self, f"{lable}"),
                "is_open": getattr(self, f"{lable}_is_open")
            }

        return user_data
    
    def get_data_with_secret(self):
        lables = ["profession", "age", "hobby", "item", "fact", "health"]
        user_data = {}

        for lable in lables:
            if getattr(self, f"{lable}_is_open"):
                user_data[lable] = {
                    "value": getattr(self, f"{lable}"),
                }
                continue
            
            user_data[lable] = {
                    "value": "",
            }

        return user_data

            


