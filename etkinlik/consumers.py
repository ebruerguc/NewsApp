from channels.generic.websocket import AsyncWebsocketConsumer
import json

class DuyuruConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("duyurular", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("duyurular", self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        pass
    
    async def send_duyuru(self, event):
        await self.send(text_data=json.dumps({
            'type': 'duyuru',
            'message': event['message'],
        }))

class HaberConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.channel_layer.group_add("haberler", self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard("haberler", self.channel_name)
        await self.accept()

    async def receive(self, text_data):
        pass

    async def send_haber(self, event):
        await self.send(text_data=json.dumps({
            'type': 'haber',
            'message': event['message'],
        }))  


    