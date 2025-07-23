from django.db.models.signals import post_save
from django.dispatch import receiver
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
from .models import Haber, Duyuru
import json


@receiver(post_save, sender=Haber)
def haber_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        
        # Haber verilerini hazırla
        haber_data = {
            'id': instance.id,
            'baslik': instance.baslik,
            'icerik': instance.icerik[:200] + '...' if len(instance.icerik) > 200 else instance.icerik,
            'yayin_tarihi': instance.yayin_tarihi.strftime('%d.%m.%Y') if instance.yayin_tarihi else '',
            'yazar': instance.yazar.get_full_name() if instance.yazar else 'Anonim',
        }
        
        # Tüm WebSocket gruplarına yeni haber bildirimini gönder
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'new_news',
                'data': haber_data
            }
        )
        
        # Haber güncellemeleri grubuna da gönder
        async_to_sync(channel_layer.group_send)(
            'news_updates',
            {
                'type': 'news_message',
                'message': {
                    'type': 'new_news',
                    'data': haber_data
                }
            }
        )


@receiver(post_save, sender=Duyuru)
def duyuru_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        
        # Duyuru verilerini hazırla
        duyuru_data = {
            'id': instance.id,
            'baslik': instance.baslik,
            'icerik': instance.icerik[:200] + '...' if len(instance.icerik) > 200 else instance.icerik,
            'yayin_tarihi': instance.yayin_tarihi.strftime('%d.%m.%Y') if instance.yayin_tarihi else '',
            'yazar': instance.yazar.get_full_name() if instance.yazar else 'Anonim',
        }
        
        # Tüm WebSocket gruplarına yeni duyuru bildirimini gönder
        async_to_sync(channel_layer.group_send)(
            'notifications',
            {
                'type': 'new_announcement',
                'data': duyuru_data
            }
        )
        
        # Duyuru güncellemeleri grubuna da gönder
        async_to_sync(channel_layer.group_send)(
            'announcement_updates',
            {
                'type': 'announcement_message',
                'message': {
                    'type': 'new_announcement',
                    'data': duyuru_data
                }
            }
        )