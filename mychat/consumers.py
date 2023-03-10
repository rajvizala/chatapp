from email import message
import json
from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
""" 
class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_group_name = 'test'
        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )
        self.accept()
       

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        print("message",message)

        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,{
                'type':"chat_message",
                'message':message
            }
        )

    def chat_message(self,event):
        message = event['message']
        self.send(text_data=json.dumps({
            'type':'chat',
            'message':message
            }
        ))
     """    

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = "chat_%s" % self.room_name
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_name = text_data_json['user_name']
        await self.channel_layer.group_send(
            self.room_group_name,
            {
            'type':'chat_message',
            'message':message,
            'user_name':user_name,
            }
        )

    async def chat_message(self,event):
        message = event['message']
        user_name = event['user_name']
        await self.send(text_data=json.dumps({
            'message':message,
            'user_name':user_name,  #This data is send to chatRoom.send() method in html page 
        }))