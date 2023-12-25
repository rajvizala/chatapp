from email import message
import json

from channels.generic.websocket import WebsocketConsumer,AsyncWebsocketConsumer
from asgiref.sync import async_to_sync
import spacy

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
        print("\n\nNEW USER LOGGED IN!!")
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = "chat_%s" % self.room_name
        print("ROOM :", self.room_name, self.room_group_name)
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()
        user_name = self.scope.get("user")
        print("USERNAME:", user_name.username, type(user_name.username))
        await self.channel_layer.group_send(self.room_group_name,
                                             {"type":"logged_in", "login_msg": "Someone Logged In!", 'user_name':user_name.username})

    async def logged_in(self, event):
        msg = event['login_msg']
        username = event['user_name']
        await self.send(text_data=json.dumps({
            'login_msg':msg,
            'username':username
        }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
       
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user_name = text_data_json['user_name']
        print("User Name", user_name)
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
        print("Message Recieved From Chat Box:", message)
        if message.strip().upper().startswith("ANALYSE"):
            nlp = spacy.load("en_core_web_sm")
            analysis_text = message[len("ANALYSE"):].strip()
            print(analysis_text)
            doc = nlp(analysis_text)
            # Extract POS tags for each token in the sentence
            pos_tags = [(token.text, token.pos_) for token in doc]
            pos_dict = {}
            # Populate the dictionary
            for word, pos_tag in pos_tags:
                pos_dict[word] = pos_tag
            print("Dict", pos_dict)
            user_name = event['user_name']
            await self.send(text_data=json.dumps({
                'message':pos_dict,
                'user_name':user_name,  #This data is send to chatRoom.send() method in html page 
            }))

        else:
            user_name = event['user_name']
            await self.send(text_data=json.dumps({
                'message':message,
                'user_name':user_name,  #This data is send to chatRoom.send() method in html page 
            }))