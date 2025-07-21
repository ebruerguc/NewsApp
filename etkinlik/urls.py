from django.urls import path
from .views import DuyuruListView, HaberListView, DuyuruDetailView, HaberDetailView, home_page


urlpatterns = [
    path('', home_page, name='home'),
    path('duyurular/', DuyuruListView.as_view(), name='duyuru_list'),
    path('duyurular/<int:pk>/', DuyuruDetailView.as_view(), name='duyuru_detay'),
    path('haberler/', HaberListView.as_view(), name='haber_list'),
    path('haberler/<int:pk>/', HaberDetailView.as_view(), name='haber_detay'),
    
]


