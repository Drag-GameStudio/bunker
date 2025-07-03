from django.db import models
from django.apps import apps
from bunker.settings import VARIABLE_OF_STATE, VARIABLE_OF_LAP_STATE
from game.game_handler.gpt_handler import get_situation
import random

class Session(models.Model):
    id = models.AutoField(primary_key=True)
    state = models.CharField(max_length=100, default=VARIABLE_OF_STATE[0])
    line_of_user = models.CharField(max_length=1000, default="")
    current_user = models.IntegerField(default=-1)
    
    lap_state = models.CharField(max_length=100, default=VARIABLE_OF_LAP_STATE[0])
    situation = models.CharField(max_length=1000, default="")
    current_situation = models.CharField(max_length=1000, default="")
    

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

    def create_voiting(self):
        users = self.get_line()
        VoitingModel = apps.get_model("game", "Voiting")
        for user in users:
            user_class = User.objects.filter(id=user).first()
            vmu = VoitingModel(vote_user=user_class)
            vmu.session = self
            vmu.save()

        self.lap_state = VARIABLE_OF_LAP_STATE[1]
        self.save()
        
        return self.get_users_data()
    
    def get_users_data(self):
        users = self.get_line()
        res_data = {}
        for user in users:
            user_class = User.objects.filter(id=user).first()
            res_data[user_class.id] = user_class.username

        return res_data

    def is_voting_ended(self): # False = isnt end
        VoitingModel = apps.get_model("game", "Voiting")
        all_votings = VoitingModel.objects.filter(session=self).filter(vote_user__isAlive=True)

        for voting_user in list(all_votings):
            if voting_user.have_voted == False:
                return False
            
        return True
    
    def close_voting(self):
        VoitingModel = apps.get_model("game", "Voiting")
        all_votings = VoitingModel.objects.filter(session=self)

        max_data = [-1, None] #count_of_voice, user
        for voting_user in list(all_votings):
            if voting_user.count_of_voice >= max_data[0]:
                max_data = [voting_user.count_of_voice, voting_user.vote_user]

        for voting_user in list(all_votings):
            voting_user.delete()


        self.lap_state = VARIABLE_OF_LAP_STATE[0]
        self.save()

        self.kick_user(max_data[1])

        return max_data[1]

    def kick_user(self, user):
        user.isAlive = False
        user.save()

        users_id: list = self.get_line()
        users_id.pop(users_id.index(str(user.id)))
        self.set_line_of_users(users_id)

        if self.current_user == user.id:
            self.current_user = self.get_line()[0]

        self.save()

    def start_lap(self):
        
        self.current_situation = get_situation(self)
        self.save()

class User(models.Model):

    id = models.AutoField(primary_key=True)
    username = models.CharField(max_length=100)
    session = models.ForeignKey(Session, on_delete=models.CASCADE, null=True, blank=True)
    isOwner = models.BooleanField(default=False)

    isAlive = models.BooleanField(default=True)

    def __str__(self):
        return self.username
    
    def can_move(self) -> bool:
        self.session.refresh_from_db()
        return (self.session.current_user == self.id and self.isAlive) 
    
    def vote(self, vote_user_id: int):
        self.refresh_from_db()
        kick_user = None
        VoitingModel = apps.get_model("game", "Voiting")
        vote_user_data = VoitingModel.objects.filter(vote_user=self).first()
        
        if vote_user_data.have_voted == False and self.isAlive:
            vote_user_data.have_voted = True
            vote_user_data.save()

            curr_vote_user = VoitingModel.objects.filter(vote_user=User.objects.filter(id=vote_user_id).first()).first()
            curr_vote_user.count_of_voice += 1
            curr_vote_user.save()

            

        voting_status = self.session.is_voting_ended()
        if voting_status:
            kick_user = self.session.close_voting().id

        return voting_status, kick_user



    
