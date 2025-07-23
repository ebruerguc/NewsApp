import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import AnonymousUser
from .models import Haber, Duyuru


class NewsConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'news_updates'
        
        # WebSocket grubuna katıl
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        # WebSocket grubundan ayrıl
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # WebSocket'ten mesaj al
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Gruba mesaj gönder
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'news_message',
                'message': message
            }
        )
    
    # Gruptan mesaj al
    async def news_message(self, event):
        message = event['message']
        
        # WebSocket'e mesaj gönder
        await self.send(text_data=json.dumps({
            'message': message
        }))


class AnnouncementConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'announcement_updates'
        
        # WebSocket grubuna katıl
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
    async def disconnect(self, close_code):
        # WebSocket grubundan ayrıl
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # WebSocket'ten mesaj al
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Gruba mesaj gönder
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'announcement_message',
                'message': message
            }
        )
    
    # Gruptan mesaj al
    async def announcement_message(self, event):
        message = event['message']
        
        # WebSocket'e mesaj gönder
        await self.send(text_data=json.dumps({
            'message': message
        }))


class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_group_name = 'notifications'
        
        # WebSocket grubuna katıl
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        
        await self.accept()
        
        # Bağlantı kurulduğunda hoş geldin mesajı gönder
        await self.send(text_data=json.dumps({
            'type': 'connection_established',
            'message': 'WebSocket bağlantısı kuruldu!'
        }))
        
    async def disconnect(self, close_code):
        # WebSocket grubundan ayrıl
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
    
    # WebSocket'ten mesaj al
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'message')
        message = text_data_json.get('message', '')
        
        # Gruba mesaj gönder
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'send_notification',
                'message_type': message_type,
                'message': message
            }
        )
    
    # Gruptan mesaj al
    async def send_notification(self, event):
        message_type = event['message_type']
        message = event['message']
        
        # WebSocket'e mesaj gönder
        await self.send(text_data=json.dumps({
            'type': message_type,
            'message': message
        }))
    
    # Yeni haber bildirimi
    async def new_news(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_news',
            'data': event['data']
        }))
    
    # Yeni duyuru bildirimi
    async def new_announcement(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new_announcement',
            'data': event['data']
        }))