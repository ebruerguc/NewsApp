from django.db import models
from django.conf import settings
from django.contrib.auth import get_user_model
from django.urls import reverse

class Duyuru(models.Model):
    baslik = models.CharField(max_length=250, verbose_name = 'Duyuru Başlığı')
    icerik = models.TextField(verbose_name='Duyuru İçeriği')
    yayin_tarihi = models.DateField(null=True, blank=True, verbose_name='Yayın Tarihi')
    resim_url= models.ImageField(upload_to='duyuru_resim/', blank=True, null=True, verbose_name='Resim URL')
    kaynak_url = models.CharField(max_length=500, blank=True, null=True, verbose_name='Kaynak URL')
    yazar = models.ForeignKey(get_user_model(), verbose_name='Yazar', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name= 'Duyuru'
        ordering = ['-yayin_tarihi'] # son eklenen duyurunun en üstte görünmesi için

    def __str__(self):
        return self.baslik
    
    def get_absolute_url(self):
        return reverse('duyuru_detay', args=[str(self.id)])
    
class Haber(models.Model):
    baslik = models.CharField(max_length=250, verbose_name='Haber Başlığı')
    icerik = models.TextField(verbose_name='Haber İçeriği')
    yayin_tarihi = models.DateField(null=True, blank=True, verbose_name='Yayın Tarihi')
    kaynak_url = models.URLField(max_length=500, blank=True, null=True, verbose_name='Kaynak URL')
    yazar = models.ForeignKey(get_user_model(), verbose_name='Yazar', on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        verbose_name = 'Haber'
        ordering = ['-yayin_tarihi']

    def __str__(self):
        return self.baslik
    
    def get_absolute_url(self):
        return reverse('haber_detay', args=[str(self.id)])
    

        
    

    

