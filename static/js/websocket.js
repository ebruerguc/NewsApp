// WebSocket bağlantısı için yardımcı sınıf
class NewsWebSocket {
    constructor() {
        this.socket = null;
        this.reconnectInterval = 5000; // 5 saniye
        this.maxReconnectAttempts = 5;
        this.reconnectAttempts = 0;
        this.isConnected = false;
        
        this.init();
    }
    
    init() {
        this.connect();
        this.setupEventListeners();
    }
    
    connect() {
        const protocol = window.location.protocol === 'https:' ? 'wss:' : 'ws:';
        const wsUrl = `${protocol}//${window.location.host}/ws/notifications/`;
        
        this.socket = new WebSocket(wsUrl);
        
        this.socket.onopen = (event) => {
            console.log('WebSocket bağlantısı kuruldu');
            this.isConnected = true;
            this.reconnectAttempts = 0;
            this.showConnectionStatus('Bağlandı', 'success');
        };
        
        this.socket.onmessage = (event) => {
            const data = JSON.parse(event.data);
            this.handleMessage(data);
        };
        
        this.socket.onclose = (event) => {
            console.log('WebSocket bağlantısı kapandı');
            this.isConnected = false;
            this.showConnectionStatus('Bağlantı kesildi', 'error');
            this.attemptReconnect();
        };
        
        this.socket.onerror = (error) => {
            console.error('WebSocket hatası:', error);
            this.showConnectionStatus('Bağlantı hatası', 'error');
        };
    }
    
    handleMessage(data) {
        switch(data.type) {
            case 'connection_established':
                console.log('Bağlantı kuruldu:', data.message);
                break;
                
            case 'new_news':
                this.showNewsNotification(data.data);
                this.updateNewsList(data.data);
                break;
                
            case 'new_announcement':
                this.showAnnouncementNotification(data.data);
                this.updateAnnouncementsList(data.data);
                break;
                
            default:
                console.log('Bilinmeyen mesaj tipi:', data);
        }
    }
    
    showNewsNotification(newsData) {
        // Toast bildirimi göster
        this.showToast(`Yeni Haber: ${newsData.baslik}`, 'info');
        
        // Browser bildirimi (izin varsa)
        if (Notification.permission === 'granted') {
            new Notification('Yeni Haber!', {
                body: newsData.baslik,
                icon: '/static/images/news-icon.png'
            });
        }
    }
    
    showAnnouncementNotification(announcementData) {
        // Toast bildirimi göster
        this.showToast(`Yeni Duyuru: ${announcementData.baslik}`, 'warning');
        
        // Browser bildirimi (izin varsa)
        if (Notification.permission === 'granted') {
            new Notification('Yeni Duyuru!', {
                body: announcementData.baslik,
                icon: '/static/images/announcement-icon.png'
            });
        }
    }
    
    updateNewsList(newsData) {
        const newsList = document.getElementById('news-list');
        if (newsList) {
            const newsItem = this.createNewsItem(newsData);
            newsList.insertAdjacentHTML('afterbegin', newsItem);
            
            // Animasyon ekle
            const firstItem = newsList.firstElementChild;
            firstItem.classList.add('new-item-animation');
        }
    }
    
    updateAnnouncementsList(announcementData) {
        const announcementsList = document.getElementById('announcements-list');
        if (announcementsList) {
            const announcementItem = this.createAnnouncementItem(announcementData);
            announcementsList.insertAdjacentHTML('afterbegin', announcementItem);
            
            // Animasyon ekle
            const firstItem = announcementsList.firstElementChild;
            firstItem.classList.add('new-item-animation');
        }
    }
    
    createNewsItem(newsData) {
        return `
            <div class="news-item border-left-primary shadow mb-4">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-primary text-uppercase mb-1">
                                Yeni Haber - ${newsData.yayin_tarihi}
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                ${newsData.baslik}
                            </div>
                            <div class="text-gray-600 mt-2">
                                ${newsData.icerik}
                            </div>
                            <small class="text-muted">Yazar: ${newsData.yazar}</small>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-newspaper fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    createAnnouncementItem(announcementData) {
        return `
            <div class="announcement-item border-left-warning shadow mb-4">
                <div class="card-body">
                    <div class="row no-gutters align-items-center">
                        <div class="col mr-2">
                            <div class="text-xs font-weight-bold text-warning text-uppercase mb-1">
                                Yeni Duyuru - ${announcementData.yayin_tarihi}
                            </div>
                            <div class="h5 mb-0 font-weight-bold text-gray-800">
                                ${announcementData.baslik}
                            </div>
                            <div class="text-gray-600 mt-2">
                                ${announcementData.icerik}
                            </div>
                            <small class="text-muted">Yazar: ${announcementData.yazar}</small>
                        </div>
                        <div class="col-auto">
                            <i class="fas fa-bullhorn fa-2x text-gray-300"></i>
                        </div>
                    </div>
                </div>
            </div>
        `;
    }
    
    showToast(message, type = 'info') {
        // Toast container oluştur (yoksa)
        let toastContainer = document.getElementById('toast-container');
        if (!toastContainer) {
            toastContainer = document.createElement('div');
            toastContainer.id = 'toast-container';
            toastContainer.className = 'toast-container';
            document.body.appendChild(toastContainer);
        }
        
        // Toast elementi oluştur
        const toast = document.createElement('div');
        toast.className = `toast toast-${type}`;
        toast.innerHTML = `
            <div class="toast-content">
                <i class="fas fa-${this.getToastIcon(type)}"></i>
                <span>${message}</span>
                <button class="toast-close">&times;</button>
            </div>
        `;
        
        // Toast'ı ekle
        toastContainer.appendChild(toast);
        
        // Animasyon
        setTimeout(() => toast.classList.add('show'), 100);
        
        // Otomatik kaldırma
        setTimeout(() => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        }, 5000);
        
        // Manuel kapatma
        toast.querySelector('.toast-close').onclick = () => {
            toast.classList.remove('show');
            setTimeout(() => toast.remove(), 300);
        };
    }
    
    getToastIcon(type) {
        const icons = {
            'success': 'check-circle',
            'error': 'exclamation-circle',
            'warning': 'exclamation-triangle',
            'info': 'info-circle'
        };
        return icons[type] || 'info-circle';
    }
    
    showConnectionStatus(message, type) {
        const statusElement = document.getElementById('connection-status');
        if (statusElement) {
            statusElement.textContent = message;
            statusElement.className = `connection-status ${type}`;
        }
    }
    
    attemptReconnect() {
        if (this.reconnectAttempts < this.maxReconnectAttempts) {
            this.reconnectAttempts++;
            console.log(`Yeniden bağlanma denemesi ${this.reconnectAttempts}/${this.maxReconnectAttempts}`);
            
            setTimeout(() => {
                this.connect();
            }, this.reconnectInterval);
        } else {
            console.log('Maksimum yeniden bağlanma denemesi aşıldı');
            this.showConnectionStatus('Bağlantı başarısız', 'error');
        }
    }
    
    setupEventListeners() {
        // Sayfa kapatılırken WebSocket'i kapat
        window.addEventListener('beforeunload', () => {
            if (this.socket) {
                this.socket.close();
            }
        });
        
        // Browser bildirimi izni iste
        if ('Notification' in window && Notification.permission === 'default') {
            Notification.requestPermission();
        }
    }
    
    // Manuel mesaj gönderme
    sendMessage(message, type = 'message') {
        if (this.isConnected && this.socket) {
            this.socket.send(JSON.stringify({
                type: type,
                message: message
            }));
        } else {
            console.warn('WebSocket bağlantısı yok');
        }
    }
}

// WebSocket'i başlat
let newsWebSocket;

document.addEventListener('DOMContentLoaded', function() {
    newsWebSocket = new NewsWebSocket();
    
    // Bağlantı durumu göstergesi ekle
    const statusIndicator = document.createElement('div');
    statusIndicator.innerHTML = `
        <div id="connection-status" class="connection-status connecting">
            Bağlanıyor...
        </div>
    `;
    document.body.appendChild(statusIndicator);
});

// Global fonksiyonlar
window.sendTestMessage = function(message) {
    if (newsWebSocket) {
        newsWebSocket.sendMessage(message, 'test');
    }
};

window.getConnectionStatus = function() {
    return newsWebSocket ? newsWebSocket.isConnected : false;
};