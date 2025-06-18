from channels.generic.websocket import AsyncWebsocketConsumer
import json
from .models import User, Session
from asgiref.sync import sync_to_async
import json

class LobbyConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        headers = dict(self.scope["headers"])
        cookies = headers.get(b"cookie", b"").decode()
        cookie_dict = dict(cookie.strip().split("=") for cookie in cookies.split("; ") if "=" in cookie)
        user_id = cookie_dict["user_id"]

        user = await self.get_user(user_id)
        if user is None:
            await self.close(code=4000)
            return
        
        self.user = user

        self.group_name = f"lobby_{await self.get_user_session_id(self.user)}"
        self.individual_group_name = f"user_{self.user.id}"

        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "join",
                "name": self.user.username,
                "user_id": self.user.id
            }
        )

        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.channel_layer.group_add(self.individual_group_name, self.channel_name)

        user_names, users_id = await self.get_all_user_of_session(await self.get_user_session(self.user))
        await self.channel_layer.group_send(
            self.individual_group_name,
            {
                "type": "load_all_users",
                "user_names": user_names,
                "users_id": users_id
            }
        )

        await self.accept()



    async def disconnect(self, close_code):
        await self.channel_layer.group_send(
            self.group_name,
            {
                "type": "disconect_user",
                "name": self.user.username,
                "user_id": self.user.id
            })
        
        await self.channel_layer.group_discard(
            self.group_name,
            self.channel_name
        )

        await self.channel_layer.group_discard(
            self.individual_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        json_data = json.loads(text_data)

    @sync_to_async
    def get_user(self, user_id):
        return User.objects.filter(id=user_id).first()
    
    

    @sync_to_async
    def get_user_session(self, user: User) -> Session:
        return user.session
    
    @sync_to_async
    def get_user_session_id(self, user: User) -> int:
        return user.session.id
    
    @sync_to_async
    def get_all_user_of_session(self, session: Session):
        all_users = User.objects.filter(session=session)

        names = [current_user.username for current_user in all_users]
        ids = [current_user.id for current_user in all_users]

        return names, ids
    
    async def join(self, event):
        name = event.get("name")
        user_id = event.get("user_id")

        await self.send(text_data=json.dumps({
            "type": "join",
            "username": name,
            "user_id": user_id
        }))

    async def disconect_user(self, event):
        name = event.get("name")
        user_id = event.get("user_id")

        await self.send(text_data=json.dumps({
            "type": "disconect_user",
            "username": name,
            "user_id": user_id
        }))

    async def load_all_users(self, event):
        users_name = event.get("user_names")
        users_id = event.get("users_id")


        await self.send(text_data=json.dumps({
            "type": "load",
            "usernames": users_name,
            "users_id": users_id
        }))