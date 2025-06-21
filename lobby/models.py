from django.db import models
from bunker.settings import VARIABLE_OF_STATE


class Session(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=100, default=VARIABLE_OF_STATE[0])
    line_of_user = models.CharField(max_length=1000, default="")
    current_user = models.IntegerField(default=-1)

    def __str__(self):
        return str(self.id)
    
    def set_line_of_users(self, users_id):
        self.line_of_user = ",".join([str(user_id) for user_id in users_id])
        self.save()

    def get_line(self):
        if self.line_of_user == "":
            return []
        
        return self.line_of_user.split(",")
    
    def next_user_in_line(self) -> bool:
        user_line = self.get_line()
        curent_user_id = self.current_user
        user_index = user_line.index(str(curent_user_id))
        
        if user_index + 1 > len(user_line) - 1:
            self.current_user = user_line[0]
            self.save()
            return False
        
        self.current_user = user_line[user_index + 1]
        self.save()

        return True

class User(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    isOwner = models.BooleanField(default=False)

    def __str__(self):
        return self.username
    
    def can_move(self) -> bool:
        self.session.refresh_from_db()
        return self.session.current_user == self.id
    
