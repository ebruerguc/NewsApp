from django.contrib import admin
from .models import Duyuru, Haber

@admin.register(Duyuru)
class DuyuruAdmin(admin.ModelAdmin):
    list_display= ('baslik', 'yayin_tarihi', 'yazar', 'resim_url')
    search_fields= ('baslik', 'icerik')
    list_filter= ('yayin_tarihi',)

@admin.register(Haber)
class HaberAdmin(admin.ModelAdmin):
    list_display= ('baslik', 'yayin_tarihi', 'yazar')
    search_fields = ('baslik', 'icerik')
    list_filter= ('yayin_tarihi',)



