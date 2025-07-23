from django.urls import path
from .views import DuyuruListView, HaberListView, DuyuruDetailView, HaberDetailView, home_page, websocket_test, send_test_notification


urlpatterns = [
    path('', home_page, name='home'),
    path('duyurular/', DuyuruListView.as_view(), name='duyuru_list'),
    path('duyurular/<int:pk>/', DuyuruDetailView.as_view(), name='duyuru_detay'),
    path('haberler/', HaberListView.as_view(), name='haber_list'),
    path('haberler/<int:pk>/', HaberDetailView.as_view(), name='haber_detay'),
    path('websocket-test/', websocket_test, name='websocket_test'),
    path('api/send-notification/', send_test_notification, name='send_test_notification'),
]


