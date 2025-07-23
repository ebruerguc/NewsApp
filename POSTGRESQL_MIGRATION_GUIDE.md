# PostgreSQL'e Geçiş Kılavuzu

Bu kılavuz, WebSocket özelliklerini PostgreSQL ile kullanmak için gerekli adımları açıklar.

## 🚨 Önemli Not

Bu test ortamında PostgreSQL mevcut olmadığı için geçici olarak SQLite kullandık. Ancak production ortamınızda PostgreSQL kullanmanız önerilir.

## 📝 PostgreSQL'e Geçiş Adımları

### 1. PostgreSQL Kurulumu (Production Sunucunuzda)

```bash
# Ubuntu/Debian
sudo apt update
sudo apt install postgresql postgresql-contrib

# PostgreSQL'i başlatın
sudo systemctl start postgresql
sudo systemctl enable postgresql
```

### 2. Veritabanı ve Kullanıcı Oluşturma

```bash
# PostgreSQL kullanıcısına geçin
sudo -u postgres psql

# Veritabanı oluşturun
CREATE DATABASE newsapp;

# Kullanıcı oluşturun
CREATE USER newsapp_user WITH PASSWORD 'güçlü_şifre_buraya';

# Yetkileri verin
GRANT ALL PRIVILEGES ON DATABASE newsapp TO newsapp_user;

# Çıkış
\q
```

### 3. Django Settings Güncellemesi

`newsapp/settings.py` dosyasında:

```python
# SQLite ayarlarını kaldırın ve PostgreSQL'i etkinleştirin
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
    }
}
```

### 4. .env Dosyası Güncellemesi

```env
DB_NAME=newsapp
DB_USER=newsapp_user
DB_PASSWORD=güçlü_şifre_buraya
DB_HOST=localhost
DB_PORT=5432
```

### 5. Gerekli Paketlerin Kurulumu

```bash
pip install psycopg2-binary
```

### 6. Migrasyon İşlemleri

```bash
# Migrasyon dosyalarını oluşturun
python manage.py makemigrations

# Migrasyon uygulayın
python manage.py migrate

# Süper kullanıcı oluşturun
python manage.py createsuperuser
```

## 🔄 Mevcut SQLite Verilerini PostgreSQL'e Aktarma

### Yöntem 1: Django Fixtures Kullanma

```bash
# SQLite'dan veri dışa aktarın
python manage.py dumpdata --natural-foreign --natural-primary > data.json

# PostgreSQL ayarlarına geçin
# settings.py'de DATABASES'i PostgreSQL'e çevirin

# Migrasyon yapın
python manage.py migrate

# Veriyi içe aktarın
python manage.py loaddata data.json
```

### Yöntem 2: pgloader Kullanma (Gelişmiş)

```bash
# pgloader kurulumu
sudo apt install pgloader

# SQLite'dan PostgreSQL'e aktarım
pgloader sqlite:///path/to/db.sqlite3 postgresql://user:password@localhost/newsapp
```

## 🚀 Production Ortamı için Öneriler

### 1. Redis Kurulumu (WebSocket için)

```bash
# Redis kurulumu
sudo apt install redis-server

# Redis'i başlatın
sudo systemctl start redis-server
sudo systemctl enable redis-server
```

### 2. Settings.py'de Redis Yapılandırması

```python
# Channel Layers - Redis kullanın
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
        },
    },
}
```

### 3. ASGI Server (Daphne)

```bash
# Daphne kurulumu
pip install daphne

# Sunucuyu başlatın
daphne -b 0.0.0.0 -p 8000 newsapp.asgi:application
```

### 4. Nginx Yapılandırması

```nginx
server {
    listen 80;
    server_name your-domain.com;

    # Static dosyalar
    location /static/ {
        alias /path/to/your/staticfiles/;
    }

    # Media dosyalar
    location /media/ {
        alias /path/to/your/media/;
    }

    # WebSocket
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

    # HTTP istekleri
    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

## 🔧 WebSocket Özellikleri PostgreSQL ile

WebSocket özellikleri veritabanından bağımsız çalışır, ancak:

1. **Signals** - Haber/duyuru ekleme işlemleri PostgreSQL'de saklanır
2. **User Authentication** - Kullanıcı yetkilendirmesi PostgreSQL üzerinden
3. **Message History** - İsteğe bağlı olarak mesaj geçmişi PostgreSQL'de saklanabilir

## 📊 Performans Optimizasyonları

### PostgreSQL için:

```python
# settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config('DB_NAME'),
        'USER': config('DB_USER'),
        'PASSWORD': config('DB_PASSWORD'),
        'HOST': config('DB_HOST'),
        'PORT': config('DB_PORT'),
        'OPTIONS': {
            'MAX_CONNS': 20,
            'OPTIONS': {
                '-c default_transaction_isolation=read_committed',
            }
        }
    }
}
```

### Redis için:

```python
CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [('127.0.0.1', 6379)],
            "capacity": 1500,
            "expiry": 60,
        },
    },
}
```

## 🧪 Test Etme

PostgreSQL'e geçtikten sonra:

1. `http://your-domain.com/websocket-test/` sayfasını ziyaret edin
2. WebSocket bağlantısının çalıştığını kontrol edin
3. Admin panelinden yeni haber/duyuru ekleyin
4. Gerçek zamanlı bildirimlerin geldiğini doğrulayın

## 🆘 Sorun Giderme

### PostgreSQL Bağlantı Hatası
```bash
# PostgreSQL durumunu kontrol edin
sudo systemctl status postgresql

# Log'ları kontrol edin
sudo tail -f /var/log/postgresql/postgresql-*.log
```

### WebSocket Bağlantı Hatası
```bash
# Redis durumunu kontrol edin
redis-cli ping

# Daphne log'larını kontrol edin
```

---

**💡 Not:** Bu test ortamında SQLite kullandık, ancak production ortamınızda yukarıdaki adımları takip ederek PostgreSQL'e geçebilirsiniz. WebSocket özellikleri her iki veritabanı ile de aynı şekilde çalışacaktır.