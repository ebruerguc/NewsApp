from django.shortcuts import render
from django.views.generic import TemplateView 

def home_view(request):
    return render(request, 'home.html')



class HomePageView(TemplateView):
    template_name='home.html'
