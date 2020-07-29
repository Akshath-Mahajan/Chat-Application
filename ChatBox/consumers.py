from channels.consumer import AsyncConsumer, SyncConsumer
import asyncio
from .models import ChatMessage, Thread
import channels
from django.contrib.auth.models import User
from channels.db import database_sync_to_async
import json
class ChatConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        await self.send({
            'type':'websocket.accept'
        })
        user_one = self.scope['user']
        user_two = await self.get_user()
        thread = await self.get_thread(user_one, user_two)
        self.thread = thread
        chat_room_name = str(thread.id)
        self.chat_room = chat_room_name
        await self.channel_layer.group_add(chat_room_name, self.channel_name)
        
    async def websocket_receive(self, event):
        user = self.scope['user'].username
        txt = event['text']
        await self.create_msg(message=txt)
        txt = json.dumps({'text':txt, 'username':user})
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
        c = ChatMessage(user = user, text= message, thread=self.thread)
        c.save()
    @database_sync_to_async
    def get_thread(self, user_one, user_two):
        return Thread.objects.get_thread_or_create(user1=user_one, user2=user_two)
    @database_sync_to_async
    def get_user(self):
        return User.objects.get(username=self.scope['url_route']['kwargs']['username'])