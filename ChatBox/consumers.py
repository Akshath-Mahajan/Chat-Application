from channels.consumer import AsyncConsumer, SyncConsumer
import asyncio
from .models import ChatMessage, Thread
import channels
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("Connect: we are here")
        await self.send({
            'type':'websocket.accept'
        })
        user_one = self.scope['user']
        user_two = await self.get_user()
        print(user_one, user_two)
        thread = await self.get_thread(user_one, user_two)
        print(thread)
        self.thread = thread
        chat_room_name = str(thread.id)
        self.chat_room = chat_room_name
        await self.channel_layer.group_add(chat_room_name, self.channel_name)
        
    async def websocket_receive(self, event):
        print("Recieve", event)
        user = self.scope['user'].username
        txt = event['text']
        await self.create_msg(message=txt)
        await self.channel_layer.group_send(
                self.chat_room,
                {
                    "type": "send_to_thread",
                    "text": txt
                }
            )
    async def send_to_thread(self, event):
        await self.send({
            'type':'websocket.send',
            'text': event['text']
        })
    async def websocket_disconnect(self, event):
        pass
    @database_sync_to_async
    def create_msg(self, message):
        user = self.scope['user']
        c = ChatMessage(user = user, text= message)
        c.save()
    @database_sync_to_async
    def get_thread(self, user_one, user_two):
        return Thread.objects.get_thread_or_create(user1=user_one, user2=user_two)
    @database_sync_to_async
    def get_user(self):
        return User.objects.get(username='TESTDUMMY')