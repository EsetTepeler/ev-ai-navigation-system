# Kurulum Kılavuzu

Bu kılavuz, EV AI Navigation System'ın yerel ortamda kurulumu için adım adım talimatlar içerir.

## 📋 Gereksinimler

### Yazılım Gereksinimleri

| Yazılım | Minimum Versiyon | Önerilen |
|---------|------------------|----------|
| Python | 3.9 | 3.11+ |
| Node.js | 18 | 20+ |
| npm | 9 | 10+ |
| Docker | 20.10 | Latest |
| Docker Compose | 2.0 | Latest |

### Sistem Gereksinimleri

- **RAM**: Minimum 4GB, Önerilen 8GB+
- **Disk**: Minimum 5GB boş alan
- **OS**: Windows 10/11, macOS 10.15+, Ubuntu 20.04+

### API Anahtarları

- OpenAI API Key veya OpenRouter API Key (AI özellikleri için)

---

## 🚀 Kurulum Adımları

### 1. Repository'yi Klonlayın

```bash
git clone https://github.com/yourusername/ev-ai-navigation-system.git
cd ev-ai-navigation-system
```

### 2. Environment Dosyasını Oluşturun

Proje kök dizininde `.env` dosyası oluşturun:

```env
# ============================================
# AI CONFIGURATION
# ============================================
# OpenAI API Key (veya OpenRouter)
OPENAI_API_KEY=sk-your-api-key-here

# OpenRouter kullanıyorsanız base URL'i değiştirin
OPENAI_BASE_URL=https://openrouter.ai/api/v1

# Model seçimi
# OpenAI: gpt-4o-mini, gpt-4o, gpt-4-turbo
# OpenRouter: nvidia/nemotron-nano-9b-v2:free (ücretsiz)
OPENAI_MODEL=gpt-4o-mini

# ============================================
# DATABASE CONFIGURATION
# ============================================
DATABASE_URL=postgresql+asyncpg://postgres:postgres123@localhost:5432/ev_navigation

# ============================================
# REDIS CONFIGURATION
# ============================================
REDIS_URL=redis://localhost:6379

# ============================================
# CORS CONFIGURATION
# ============================================
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174,http://localhost:3000
```

### 3. Docker Servislerini Başlatın

PostgreSQL ve Redis containerlarını başlatın:

```bash
docker-compose up -d
```

Servislerin çalıştığını doğrulayın:

```bash
docker-compose ps
```

Beklenen çıktı:
```
NAME                  STATUS              PORTS
ev-navigation-db      Up                  0.0.0.0:5432->5432/tcp
ev-navigation-redis   Up                  0.0.0.0:6379->6379/tcp
```

### 4. Python Virtual Environment Oluşturun

#### Windows (PowerShell)
```powershell
python -m venv venv_new
.\venv_new\Scripts\Activate.ps1
```

#### Linux/macOS
```bash
python3 -m venv venv_new
source venv_new/bin/activate
```

### 5. Python Bağımlılıklarını Yükleyin

```bash
pip install -r requirements.txt
```

### 6. Backend'i Başlatın

```bash
cd backend
uvicorn orchestrator:app --host 0.0.0.0 --port 8000 --reload
```

Backend çalıştığını test edin:
```bash
curl http://localhost:8000
```

Beklenen yanıt:
```json
{"name": "EV Navigation API", "version": "2.0", "status": "active"}
```

### 7. Frontend Bağımlılıklarını Yükleyin

Yeni bir terminal açın:

```bash
cd frontend/react_app
npm install
```

### 8. Frontend'i Başlatın

```bash
npm run dev
```

Frontend'e erişin: http://localhost:5173

---

## 🔍 Kurulum Doğrulama

### API Endpoints Test

```bash
# Sistem durumu
curl http://localhost:8000

# Veritabanı bağlantısı
curl http://localhost:8000/api/test-db

# Araçlar
curl http://localhost:8000/api/vehicles-db

# Şarj istasyonları
curl http://localhost:8000/api/charging/stations
```

### Frontend Kontrol Listesi

- [ ] Harita yükleniyor mu?
- [ ] "Backend Connected" yazısı görünüyor mu?
- [ ] Şarj istasyonu marker'ları haritada görünüyor mu?
- [ ] Araç arama çalışıyor mu?

---

## 🐳 Docker ile Tam Kurulum (Alternatif)

Tüm servisleri Docker ile çalıştırmak için:

```bash
# Build
docker-compose -f docker-compose.full.yml build

# Başlat
docker-compose -f docker-compose.full.yml up -d
```

---

## ⚠️ Sık Karşılaşılan Sorunlar

### 1. Port Çakışması

**Sorun**: Port 5432 veya 6379 zaten kullanımda.

**Çözüm**:
```bash
# Hangi process port'u kullanıyor?
netstat -ano | findstr :5432

# Process'i sonlandır
taskkill /PID <pid> /F
```

### 2. Database Bağlantı Hatası

**Sorun**: `Connection refused to localhost:5432`

**Çözüm**:
```bash
# Docker container çalışıyor mu?
docker-compose ps

# Log'ları kontrol et
docker-compose logs db
```

### 3. OpenAI API Hatası

**Sorun**: `OpenAI API key not found`

**Çözüm**:
- `.env` dosyasında `OPENAI_API_KEY` tanımlı mı kontrol edin
- API anahtarınızın geçerli olduğunu doğrulayın
- OpenRouter kullanıyorsanız `OPENAI_BASE_URL`'i ayarlayın

### 4. CORS Hatası

**Sorun**: Frontend'den backend'e istek yapılamıyor.

**Çözüm**:
`.env` dosyasında `ALLOWED_ORIGINS`'e frontend URL'inizi ekleyin:
```env
ALLOWED_ORIGINS=http://localhost:5173,http://localhost:5174
```

### 5. Node Modülleri Yüklenmiyor

**Sorun**: `npm install` hata veriyor.

**Çözüm**:
```bash
# node_modules'ü temizle
rm -rf node_modules package-lock.json

# Tekrar yükle
npm install
```

---

## 📦 Üretim Ortamı Yapılandırması

### Environment Variables

```env
# Production .env
NODE_ENV=production
DATABASE_URL=postgresql+asyncpg://user:password@production-db:5432/ev_nav
REDIS_URL=redis://production-redis:6379
ALLOWED_ORIGINS=https://yourdomain.com
```

### Frontend Build

```bash
cd frontend/react_app
npm run build
```

Build çıktısı `dist/` klasöründe oluşur.

### Nginx Yapılandırması

```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Frontend
    location / {
        root /var/www/ev-navigation/frontend/dist;
        try_files $uri $uri/ /index.html;
    }

    # API Proxy
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

---

## 📞 Destek

Sorunlar için GitHub Issues kullanın veya dokümantasyonu kontrol edin.
