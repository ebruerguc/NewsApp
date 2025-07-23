# Django WebSocket Entegrasyonu - Kullanım Kılavuzu

Bu kılavuz, Django projenize eklenen WebSocket özelliklerinin nasıl kullanılacağını açıklar.

## 🚀 Kurulum Tamamlandı!

Projenize aşağıdaki özellikler başarıyla eklendi:

### ✅ Eklenen Özellikler

1. **Django Channels** - WebSocket desteği
2. **Gerçek Zamanlı Bildirimler** - Yeni haber ve duyuru bildirimleri
3. **Otomatik Signals** - Admin panelinden eklenen içerik otomatik olarak yayınlanır
4. **Modern UI** - Toast bildirimleri ve animasyonlar
5. **Test Paneli** - WebSocket bağlantısını test etmek için

## 📋 Dosya Yapısı

```
newsapp/
├── newsapp/
│   ├── asgi.py (✅ Güncellendi - WebSocket routing)
│   └── settings.py (✅ Güncellendi - Channels ayarları)
├── etkinlik/
│   ├── consumers.py (🆕 Yeni - WebSocket consumer'ları)
│   ├── routing.py (🆕 Yeni - WebSocket URL routing)
│   ├── signals.py (🆕 Yeni - Otomatik bildirimler)
│   ├── views.py (✅ Güncellendi - Test view'ları)
│   └── urls.py (✅ Güncellendi - Test URL'leri)
├── static/
│   ├── js/
│   │   └── websocket.js (🆕 Yeni - Frontend WebSocket kodu)
│   └── css/
│       └── websocket.css (🆕 Yeni - WebSocket stilleri)
└── templates/
    └── websocket_test.html (🆕 Yeni - Test sayfası)
```

## 🔧 Nasıl Çalışır?

### 1. WebSocket Bağlantısı
- Kullanıcı sayfayı açtığında otomatik olarak WebSocket bağlantısı kurulur
- Bağlantı durumu sağ üst köşede gösterilir
- Bağlantı kesilirse otomatik olarak yeniden bağlanmaya çalışır

### 2. Otomatik Bildirimler
- Admin panelinden yeni haber/duyuru eklendiğinde
- Django signals otomatik olarak tetiklenir
- WebSocket üzerinden tüm bağlı kullanıcılara bildirim gönderilir

### 3. Frontend Güncellemeleri
- Yeni içerik sayfaya otomatik olarak eklenir
- Toast bildirimleri gösterilir
- Browser bildirimleri (izin verilmişse)

## 🧪 Test Etme

### 1. Test Sayfasına Erişim
```
http://localhost:8000/websocket-test/
```

### 2. Test Senaryoları

#### A) Manuel Test Mesajı
1. Test sayfasında mesaj yazın
2. "Test Mesajı Gönder" butonuna tıklayın
3. Mesajın gönderilip alındığını kontrol edin

#### B) Haber Simülasyonu
1. "Haber Simülasyonu" butonuna tıklayın
2. Yeni haber kartının oluştuğunu görün
3. Toast bildiriminin çıktığını kontrol edin

#### C) Duyuru Simülasyonu
1. "Duyuru Simülasyonu" butonuna tıklayın
2. Yeni duyuru kartının oluştuğunu görün
3. Toast bildiriminin çıktığını kontrol edin

#### D) Gerçek Test
1. Admin paneline giriş yapın: `http://localhost:8000/admin/`
2. Yeni bir haber veya duyuru ekleyin
3. Test sayfasında otomatik bildirimin geldiğini kontrol edin

## 🎨 Frontend Entegrasyonu

### Mevcut Sayfalarınıza WebSocket Eklemek

1. **JavaScript dosyasını dahil edin:**
```html
<script src="/static/js/websocket.js"></script>
```

2. **CSS dosyasını dahil edin:**
```html
<link href="/static/css/websocket.css" rel="stylesheet">
```

3. **HTML'de gerekli ID'leri ekleyin:**
```html
<!-- Haberler için -->
<div id="news-list">
    <!-- Mevcut haberleriniz -->
</div>

<!-- Duyurular için -->
<div id="announcements-list">
    <!-- Mevcut duyurularınız -->
</div>
```

### Özel Bildirim Handler'ları

JavaScript'te özel işlemler için:

```javascript
// WebSocket mesajlarını dinle
document.addEventListener('DOMContentLoaded', function() {
    if (window.newsWebSocket) {
        const originalHandleMessage = newsWebSocket.handleMessage;
        newsWebSocket.handleMessage = function(data) {
            // Orijinal fonksiyonu çağır
            originalHandleMessage.call(this, data);
            
            // Özel işlemlerinizi ekleyin
            if (data.type === 'new_news') {
                console.log('Yeni haber geldi:', data.data);
                // Özel işlemler...
            }
        };
    }
});
```

## 🔧 Yapılandırma

### WebSocket URL'leri
```python
# etkinlik/routing.py
websocket_urlpatterns = [
    re_path(r'ws/news/$', consumers.NewsConsumer.as_asgi()),
    re_path(r'ws/announcements/$', consumers.AnnouncementConsumer.as_asgi()),
    re_path(r'ws/notifications/$', consumers.NotificationConsumer.as_asgi()),
]
```

### Channel Layers (Production için)
```python
# newsapp/settings.py
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

## 🐛 Sorun Giderme

### 1. WebSocket Bağlantı Hatası
- Sunucunun çalıştığından emin olun
- Browser konsolunu kontrol edin
- ASGI server kullandığınızdan emin olun

### 2. Bildirimler Gelmiyor
- Django signals'ın aktif olduğunu kontrol edin
- Admin panelinden yeni içerik eklemeyi deneyin
- Browser konsolunda hata mesajlarını kontrol edin

### 3. CSS/JS Dosyaları Yüklenmiyor
- `python manage.py collectstatic` komutunu çalıştırın
- Static dosya ayarlarını kontrol edin

## 📱 Browser Bildirimleri

Kullanıcılardan bildirim izni istemek için:

```javascript
// Otomatik olarak çalışır, manuel olarak da çağırabilirsiniz
if ('Notification' in window && Notification.permission === 'default') {
    Notification.requestPermission();
}
```

## 🚀 Production Notları

### 1. Redis Kurulumu
```bash
# Ubuntu/Debian
sudo apt install redis-server

# Redis'i başlatın
sudo systemctl start redis-server
```

### 2. ASGI Server (Daphne)
```bash
pip install daphne
daphne -b 0.0.0.0 -p 8000 newsapp.asgi:application
```

### 3. Nginx Yapılandırması
```nginx
location /ws/ {
    proxy_pass http://127.0.0.1:8000;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
}
```

## 🎯 Gelişmiş Özellikler

### 1. Kullanıcı Grupları
Belirli kullanıcı gruplarına özel bildirimler göndermek için consumer'ları genişletebilirsiniz.

### 2. Mesaj Geçmişi
WebSocket mesajlarını veritabanında saklayarak geçmiş bildirimleri gösterebilirsiniz.

### 3. Push Notifications
Service Worker ile mobil push bildirimleri ekleyebilirsiniz.

## 📞 Destek

WebSocket entegrasyonu ile ilgili sorunlarınız için:
1. Browser konsolunu kontrol edin
2. Django log'larını inceleyin
3. Test sayfasını kullanarak bağlantıyı test edin

---

**🎉 Tebrikler!** Django projenize başarıyla WebSocket desteği eklendi. Artık kullanıcılarınız gerçek zamanlı haber ve duyuru bildirimlerini alabilir!