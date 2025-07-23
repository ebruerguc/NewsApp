from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Duyuru, Haber
from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer

@receiver(post_save, sender=Duyuru)
def duyuru_created(sender, instance, created, **kwargs):
    if created:
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "duyurular",  
            {
                "type": "send_duyuru",
                "message": instance.baslik  
            }
        )

@receiver(post_save, sender= Haber)
def haber_created(sender, instance, created, **kwargs):
    if created:
        channel_layer= get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            "haberler",
            {
                "type": "send_haber",
                "message": instance.baslik
            }
        )