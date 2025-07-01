from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from lobby.models import User, Session
from .models import UserInfo
import json
from bunker.settings import VARIABLE_OF_LAP_STATE

# надо добавить авто отображение голосования


class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope["headers"])
        cookies = headers.get(b"cookie", b"").decode()
        cookie_dict = dict(cookie.strip().split("=") for cookie in cookies.split("; ") if "=" in cookie)
        user_id = cookie_dict["user_id"]
        self.user = await self.get_user(user_id)

        self.group_name = f"game_{await self.get_user_session_id(self.user)}"
        self.individual_group_name = f"game_user{await self.get_user_session_id(self.user)}{user_id}"

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add(self.individual_group_name, self.channel_name)

        await self.load_all(self.individual_group_name)
        
        await self.accept()

    async def receive(self, text_data):
        data = json.loads(text_data)

        if data["type"] == "load":
            await self.load_all(self.individual_group_name)

        elif data["type"] == "move":
            await self.make_move(data["move_type"], data["data"])

        elif data["type"] == "vote":
            voting_status, kick_user_id = await self.vote_on_user(data["vote_user"])
            if voting_status:
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "end_voiting",
                    }
                )
                
                await self.channel_layer.group_send(
                    f"game_user{await self.get_user_session_id(self.user)}{kick_user_id}",
                    {
                        "type": "die_user",
                    }
                )
                
                await self.load_all(self.group_name)

        elif data["type"] == "load_voting":
            res_data = await self.get_users_data()
            await self.channel_layer.group_send(
                self.individual_group_name,
                {
                    "type": "start_voting",
                    "data": res_data
                }
            )


    @sync_to_async
    def get_users_data(self):
        return self.user.session.get_users_data()

    async def load_all(self, group):
        result_data = await self.get_all_user_secret()
        game_info = await self.get_game_info()

        await self.channel_layer.group_send(
            group,
            {
                "type": "load",
                "data": result_data,
                "game_info": game_info
            }
        )

    @sync_to_async
    def get_game_info(self):
        game_info = {}

        self.user.refresh_from_db()
        self.user.session.refresh_from_db()
        game_info["current_move_user"] = self.user.session.current_user
        game_info["current_lap_state"] = self.user.session.lap_state


        return game_info

    @sync_to_async
    def get_current_lap_state(self):
        self.user.session.refresh_from_db()
        return self.user.session.lap_state

    async def make_move(self, move_type, data):
        if await self.can_move() and await self.get_current_lap_state() == VARIABLE_OF_LAP_STATE[0]:
            if move_type == "open_card":
                await self.open_card(data["str_key"])

            move_status = await self.make_move_on_session()
            await self.load_all(self.group_name)

            if move_status == False:
                users_data = await self.create_voting()

                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        "type": "start_voting",
                        "data": users_data
                    }
                )

    @sync_to_async
    def vote_on_user(self, user_vote):
        voting_status, kick_user_id = self.user.vote(user_vote)
        return voting_status, kick_user_id


    @sync_to_async
    def create_voting(self):
        return self.user.session.create_voiting()

    @sync_to_async
    def can_move(self):
        return self.user.can_move()

    @sync_to_async
    def make_move_on_session(self):
        status = self.user.session.next_user_in_line()

        return status

    @sync_to_async
    def open_card(self, str_key):
        card = UserInfo.objects.filter(user=self.user).first()
        setattr(card, f"{str_key}_is_open", True)
        card.save()
        card.refresh_from_db()

    @sync_to_async
    def get_user(self, user_id):
        return User.objects.filter(id=user_id).first()
    
    @sync_to_async
    def get_user_session_id(self, user: User) -> int:
        return user.session.id
    
    @sync_to_async
    def get_all_user_secret(self):
        all_users = User.objects.filter(session=self.user.session).filter(isAlive=True)
        all_users = list(all_users)
        

        all_info_user = [UserInfo.objects.filter(user=user).first() for user in all_users]

        return_data = {}
        for i in range(len(all_users)):
            return_data[all_users[i].id] = all_info_user[i].get_data_with_secret()
            return_data[all_users[i].id]["username"] = all_users[i].username

        return return_data
        
    async def load(self, event):
        data = event["data"]
        game_info = event["game_info"]

        await self.send(text_data=json.dumps({
            "type": "load",
            "data": data,
            "game_info": game_info
        }))

    async def start_voting(self, event):
        data = event["data"]
    
        await self.send(text_data=json.dumps({
            "type": "start_voiting",
            "data": data
        }))

    async def end_voiting(self, event):

        await self.send(text_data=json.dumps({
            "type": "end_voiting",
        }))

    async def die_user(self, event):

        await self.send(text_data=json.dumps({
            "type": "die",
        }))