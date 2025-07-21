from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.conf import settings
from django.contrib.auth.decorators import login_required 
from django.utils.decorators import method_decorator
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


    
    
    