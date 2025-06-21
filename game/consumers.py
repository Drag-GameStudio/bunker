from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from lobby.models import User, Session
from .models import UserInfo
import json

class GameConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope["headers"])
        cookies = headers.get(b"cookie", b"").decode()
        cookie_dict = dict(cookie.strip().split("=") for cookie in cookies.split("; ") if "=" in cookie)
        user_id = cookie_dict["user_id"]
        self.user = await self.get_user(user_id)

        self.group_name = f"game_{await self.get_user_session_id(self.user)}"
        self.individual_group_name = f"game_user{await self.get_user_session_id(self.user)}"

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

        return game_info

    async def make_move(self, move_type, data):
        if await self.can_move():

            if move_type == "open_card":
                await self.open_card(data["str_key"])

            move_status = await self.make_move_on_session()
            await self.load_all(self.group_name)


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
        all_users = User.objects.filter(session=self.user.session)
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
    