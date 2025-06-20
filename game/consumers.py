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

        if data["type"] == "open":
            await self.open_card(data["str_key"])
            await self.load_all(self.group_name)

        elif data["type"] == "load":
            await self.load_all(self.individual_group_name)

    async def load_all(self, group):
        result_data = await self.get_all_user_secret()
        await self.channel_layer.group_send(
            group,
            {
                "type": "load",
                "data": result_data
            }
        )


    @sync_to_async
    def open_card(self, str_key):
        card = UserInfo.objects.filter(user=self.user).first()
        setattr(card, f"{str_key}_is_open", True)
        card.save()

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

        await self.send(text_data=json.dumps({
            "type": "load",
            "data": data
        }))
    