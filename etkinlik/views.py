from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import json
from .models import Duyuru, Haber

@login_required
def home_page(request):
    return render(request, 'home.html')

@method_decorator(login_required, name='dispatch')
class DuyuruListView(ListView):
    model= Duyuru
    template_name= "duyurular/duyuru_list.html"
    context_object_name = 'duyurular'
    paginate_by = 4

    def get_queryset(self):
        return Duyuru.objects.all().order_by('-yayin_tarihi')

          
@method_decorator(login_required, name='dispatch')
class DuyuruDetailView(DetailView):
    model = Duyuru
    template_name = 'duyurular/duyuru_detail.html'
    context_object_name = 'duyuru'
    

@method_decorator(login_required, name='dispatch')
class HaberListView(ListView):
    model= Haber
    template_name= "haberler/haber_list.html"
    context_object_name = 'haberler'
    paginate_by = 15

    def get_queryset(self):
        return Haber.objects.all().order_by('-yayin_tarihi')
        

class HaberDetailView(DetailView):
    model = Haber
    template_name = 'haberler/haber_detail.html'
    context_object_name = 'haber'


def websocket_test(request):
    """WebSocket test sayfası"""
    return render(request, 'websocket_test.html')

@staff_member_required
@csrf_exempt
def send_test_notification(request):
    """Admin kullanıcıları için test bildirimi gönderme"""
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            message_type = data.get('type', 'test')
            message = data.get('message', 'Test mesajı')
            
            channel_layer = get_channel_layer()
            
            # Bildirim gönder
            async_to_sync(channel_layer.group_send)(
                'notifications',
                {
                    'type': 'send_notification',
                    'message_type': message_type,
                    'message': message
                }
            )
            
            return JsonResponse({'status': 'success', 'message': 'Bildirim gönderildi'})
            
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)})
    
    return JsonResponse({'status': 'error', 'message': 'Sadece POST istekleri kabul edilir'})