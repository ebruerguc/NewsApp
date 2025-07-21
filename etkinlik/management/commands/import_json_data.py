from django.core.management.base import BaseCommand
from django.conf import settings
import json
import os
from etkinlik.models import Haber, Duyuru
from datetime import datetime

class Command(BaseCommand):
    help= 'Json dosyalarındaki verileri veritabanına aktarır'

    def handle(self, *args, **options):
        self.import_haberler()
        self.import_duyurular()

    def import_haberler(self):
        json_file_path = os.path.join(settings.BASE_DIR, 'etkinlik', 'fixtures', 'haberler.json')
        
        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)
                
                for item in json_data:
                    fields = item.get('fields', {})
                    haber, created = Haber.objects.get_or_create(
                        pk=item.get('pk'),
                        defaults={
                            'baslik': fields.get('baslik', ''),
                            'icerik': fields.get('icerik', ''),
                            'yayin_tarihi': self.parse_date(fields.get('yayin_tarihi')),
                            'kaynak_url': fields.get('kaynak_url', ''),
                            'yazar': fields.get('yazar', '')
                        }
                    )
                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Haber eklendi: {haber.baslik}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Haber zaten mevcut: {haber.baslik}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Haber dosyası bulunamadı: {json_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Haber aktarımında hata: {str(e)}'))


    def import_duyurular(self):
        json_file_path = os.path.join(settings.BASE_DIR, 'etkinlik', 'fixtures', 'duyurular.json')

        try:
            with open(json_file_path, 'r', encoding='utf-8') as f:
                json_data = json.load(f)

                for item in json_data:
                    fields = item.get('fields', {})
                    
                    duyuru, created = Duyuru.objects.get_or_create(
                        pk=item.get('pk'),
                        defaults={
                            'baslik': fields.get('baslik', ''),
                            'icerik': fields.get('icerik', ''),
                            'yayin_tarihi': self.parse_date(fields.get('yayin_tarihi')),
                            'resim_url': fields.get('resim_url', ''),
                            'kaynak_url': fields.get('kaynak_url', ''),
                            'yazar': fields.get('yazar', '')

                        }
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Duyuru eklendi: {duyuru.baslik}'))
                    else:
                        self.stdout.write(self.style.WARNING(f'Duyuru zaten mevcut: {duyuru.baslik}'))
        except FileNotFoundError:
            self.stdout.write(self.style.ERROR(f'Duyuru dosyası bulunamadı: {json_file_path}'))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f'Duyuru aktarımında hata: {str(e)}'))

    def parse_date(self, date_string):
        if not date_string:
            return None
        
        try:
            return datetime.strptime(date_string, '%Y-%m-%d').date()
        except Exception:
            return None
    



    