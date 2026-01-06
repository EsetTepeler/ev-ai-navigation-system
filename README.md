# 🚗 EV AI Navigation System

<div align="center">

![Version](https://img.shields.io/badge/version-2.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.9+-green.svg)
![React](https://img.shields.io/badge/react-18.0-61DAFB.svg)
![License](https://img.shields.io/badge/license-MIT-lightgrey.svg)

**Türkiye için Akıllı Elektrikli Araç Navigasyon Sistemi**

*AI destekli rota planlama, 286+ şarj istasyonu ve 384+ araç modeli*

</div>

---

## 📋 İçindekiler

- [Proje Hakkında](#-proje-hakkında)
- [Özellikler](#-özellikler)
- [Teknoloji Stack](#-teknoloji-stack)
- [Kurulum](#-kurulum)
- [API Dokümantasyonu](#-api-dokümantasyonu)
- [Frontend Bileşenleri](#-frontend-bileşenleri)
- [Proje Yapısı](#-proje-yapısı)
- [Geliştirme Durumu](#-geliştirme-durumu)
- [Katkıda Bulunma](#-katkıda-bulunma)

---

## 🎯 Proje Hakkında

EV AI Navigation System, Türkiye genelinde elektrikli araç kullanıcıları için optimize edilmiş bir navigasyon sistemidir. Sistem, araç batarya kapasitesi, menzil ve şarj istasyonu konumlarını dikkate alarak en uygun rotayı hesaplar.

### Temel Kavramlar

- **Akıllı Rota Planlama**: Batarya durumuna göre şarj durakları otomatik hesaplanır
- **Gerçekçi Şarj Ağları**: Türkiye'deki gerçek şarj ağları (Sharz, GoCharge, Eşarj, ZES, vb.)
- **AI Destekli Asistan**: Doğal dil ile araç ve rota sorguları
- **OSRM Entegrasyonu**: Gerçek yol verileri ile rota çizimi

---

## ✨ Özellikler

### 🗺️ Harita ve Navigasyon
- **İnteraktif Harita**: Leaflet tabanlı tam ekran harita görünümü
- **Rota Görselleştirme**: Başlangıç-bitiş arası mavi çizgi ile rota
- **Şarj Durakları**: Rota üzerinde otomatik şarj istasyonu önerileri
- **Navigasyon Modu**: Adım adım yönlendirme ile sürüş deneyimi

### ⚡ Şarj İstasyonları
- **286+ İstasyon**: Türkiye genelinde kapsamlı kapsama
- **7 Şarj Ağı**: Sharz, GoCharge, Eşarj, Voltrun, ZES, Tesla, Aytemiz
- **Güç Seviyeleri**: 50kW - 350kW arası çeşitli seçenekler
- **Şehir Filtreleme**: İstanbul, Ankara, İzmir ve 23+ şehir
- **Yarıçap Araması**: Belirli konumdan km bazlı arama

### 🚙 Araç Veritabanı
- **384+ EV Modeli**: Tüm büyük markaların elektrikli araçları
- **Detaylı Spesifikasyonlar**: Batarya kapasitesi, menzil, şarj hızı
- **Akıllı Arama**: AI destekli araç önerileri
- **Fuzzy Matching**: Yazım hatalarına toleranslı arama

### 🤖 AI Asistan
- **Doğal Dil**: Türkçe/İngilizce soru-cevap
- **Bağlam Farkındalığı**: Araç ve istasyon bilgisi ile zenginleştirilmiş yanıtlar
- **Akıllı Öneriler**: Kullanıcı tercihlerine göre araç önerileri

---

## 🛠️ Teknoloji Stack

### Backend
| Teknoloji | Açıklama |
|-----------|----------|
| **FastAPI** | Modern Python web framework |
| **PostgreSQL** | 384+ araç modeli veritabanı |
| **Redis** | Cache ve session yönetimi |
| **OpenAI/OpenRouter** | GPT-4o-mini AI entegrasyonu |
| **OSRM** | Açık kaynak rota motoru |

### Frontend
| Teknoloji | Açıklama |
|-----------|----------|
| **React 18** | UI framework |
| **Vite** | Hızlı build ve dev server |
| **Leaflet** | İnteraktif harita kütüphanesi |
| **Axios** | HTTP istemcisi |

### DevOps
| Teknoloji | Açıklama |
|-----------|----------|
| **Docker** | Container orchestration |
| **Docker Compose** | Multi-container deployment |

---

## 🚀 Kurulum

### Gereksinimler

- Python 3.9+
- Node.js 18+
- Docker & Docker Compose
- OpenAI veya OpenRouter API Key

### Hızlı Başlangıç

#### 1. Repository'yi Klonlayın
```bash
git clone https://github.com/yourusername/ev-ai-navigation-system.git
cd ev-ai-navigation-system
```

#### 2. Environment Değişkenlerini Ayarlayın
`.env` dosyası oluşturun:
```env
# AI Configuration
OPENAI_API_KEY=your_api_key_here
OPENAI_BASE_URL=https://openrouter.ai/api/v1  # OpenRouter için
OPENAI_MODEL=gpt-4o-mini

# Database
DATABASE_URL=postgresql+asyncpg://postgres:postgres123@localhost:5432/ev_navigation

# Redis
REDIS_URL=redis://localhost:6379
```

#### 3. Docker ile Servisleri Başlatın
```bash
docker-compose up -d
```
Bu komut PostgreSQL ve Redis'i başlatır.

#### 4. Backend'i Çalıştırın
```bash
# Virtual environment oluşturun
python -m venv venv_new

# Aktif edin (Windows)
.\venv_new\Scripts\Activate.ps1

# Bağımlılıkları yükleyin
pip install -r requirements.txt

# Backend'i başlatın
cd backend
uvicorn orchestrator:app --host 0.0.0.0 --port 8000 --reload
```

#### 5. Frontend'i Çalıştırın
```bash
cd frontend/react_app
npm install
npm run dev
```

### Erişim Noktaları

| Servis | URL |
|--------|-----|
| Frontend | http://localhost:5173 |
| Backend API | http://localhost:8000 |
| API Docs (Swagger) | http://localhost:8000/docs |
| API Docs (ReDoc) | http://localhost:8000/redoc |

---

## 📡 API Dokümantasyonu

### Temel Endpoints

#### Sistem Durumu
```http
GET /
```
Sistem bilgisi ve durum kontrolü.

#### Veritabanı Testi
```http
GET /api/test-db
```
PostgreSQL bağlantı durumu.

---

### Araç Endpoints

#### Tüm Araçları Listele
```http
GET /api/vehicles-db
```
**Yanıt:**
```json
{
  "vehicles": [...],
  "total": 384
}
```

#### Akıllı Araç Araması
```http
POST /api/smart-vehicle-search
Content-Type: application/json

{
  "query": "500 km menzilli SUV öner"
}
```

---

### Şarj İstasyonu Endpoints

#### Tüm İstasyonları Listele
```http
GET /api/charging/stations
```
**Yanıt:**
```json
{
  "count": 286,
  "stations": [
    {
      "name": "Sharz İstinyePark AVM",
      "city": "İSTANBUL",
      "latitude": 41.1088,
      "longitude": 29.0223,
      "power_kw": 180,
      "connector_type": "DC Fast Charge (CCS)",
      "price_per_kwh": 0.45
    }
  ]
}
```

#### Şehre Göre Filtrele
```http
GET /api/charging/stations?city=ANKARA
```

#### Yarıçap ile Arama
```http
GET /api/charging/stations?lat=41.0082&lon=28.9784&radius=50
```
**Parametreler:**
- `lat`: Enlem
- `lon`: Boylam  
- `radius`: Kilometre cinsinden yarıçap

#### Güç Seviyesine Göre Filtrele
```http
GET /api/charging/stations?min_power=150&max_power=350
```

---

### Navigasyon Endpoints

#### Basit Rota Hesaplama
```http
POST /api/navigation/simple-route
Content-Type: application/json

{
  "start_lat": 41.0082,
  "start_lon": 28.9784,
  "end_lat": 39.9334,
  "end_lon": 32.8597,
  "vehicle_range_km": 400,
  "battery_capacity_kwh": 75,
  "current_battery_percent": 80,
  "min_charge_percent": 20
}
```

**Yanıt:**
```json
{
  "success": true,
  "route_coordinates": [[41.0082, 28.9784], ...],
  "charging_stops": [
    {
      "name": "Sharz Bolu Otoyol",
      "latitude": 40.7322,
      "longitude": 31.6089,
      "power_kw": 180,
      "charging_time_minutes": 35
    }
  ],
  "route_summary": {
    "total_distance_km": 453.2,
    "driving_time_minutes": 340,
    "charging_time_minutes": 35,
    "num_charging_stops": 1,
    "estimated_cost_tl": 45.80
  }
}
```

---

### AI Chat Endpoint

#### Sohbet
```http
POST /api/ai-chat
Content-Type: application/json

{
  "message": "İstanbul'dan Ankara'ya gidecek en uygun elektrikli araç hangisi?"
}
```

---

## 🖥️ Frontend Bileşenleri

### MapView (`MapView.jsx`)
Ana harita bileşeni. Leaflet kullanarak interaktif harita gösterir.

**Özellikler:**
- Şarj istasyonu marker'ları
- Rota çizimi
- Popup bilgi kartları
- Zoom ve pan kontrolleri

### RouteForm (`RouteForm.jsx`)
Rota planlama formu.

**Özellikler:**
- Başlangıç/bitiş noktası seçimi
- Araç seçimi (fuzzy search)
- Batarya durumu slider'ı
- Nominatim geocoding entegrasyonu

### NavigationMode (`NavigationMode.jsx`)
Adım adım navigasyon modu.

**Özellikler:**
- Aktif yönlendirme
- Sonraki dönüş bilgisi
- Kalan mesafe ve süre

### AuthModals (`AuthModals.jsx`)
Giriş/kayıt modalleri.

---

## 📁 Proje Yapısı

```
ev-ai-navigation-system/
├── 📂 backend/
│   ├── orchestrator.py          # Ana FastAPI uygulaması
│   ├── 📂 src/
│   │   ├── 📂 services/
│   │   │   ├── database_service.py
│   │   │   ├── redis_service.py
│   │   │   ├── charging_station_service.py
│   │   │   └── ai_conversation_handler.py
│   │   ├── 📂 database/
│   │   │   └── connection.py
│   │   ├── 📂 exceptions/
│   │   │   └── custom_exceptions.py
│   │   └── 📂 middleware/
│   │       └── error_handlers.py
│   └── 📂 routes/
│       ├── vehicles.py
│       ├── charging.py
│       └── navigation.py
│
├── 📂 frontend/
│   └── 📂 react_app/
│       ├── 📂 src/
│       │   ├── App.jsx
│       │   ├── api.js
│       │   └── 📂 components/
│       │       ├── MapView.jsx
│       │       ├── RouteForm.jsx
│       │       └── NavigationMode.jsx
│       ├── package.json
│       └── vite.config.js
│
├── 📂 data/
│   ├── 📂 car_models/
│   │   └── all_ev_models.csv    # 384 araç modeli
│   └── 📂 charging_stations/
│       └── charging_stations_map.csv  # 286 şarj istasyonu
│
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

## 📊 Geliştirme Durumu

### ✅ Tamamlanan
- [x] FastAPI backend orchestrator
- [x] PostgreSQL veritabanı (384 araç modeli)
- [x] Redis cache entegrasyonu
- [x] OpenAI/OpenRouter AI entegrasyonu
- [x] React frontend (Vite)
- [x] Leaflet harita entegrasyonu
- [x] Türkiye geneli şarj istasyonları (286+)
- [x] OSRM rota hesaplama
- [x] Şarj durağı optimizasyonu
- [x] Navigasyon modu
- [x] Araç arama (fuzzy matching)
- [x] Docker containerization

### 🔄 Devam Eden
- [ ] Gerçek zamanlı şarj istasyonu müsaitliği
- [ ] Kullanıcı hesap sistemi
- [ ] Rota geçmişi kaydetme

### 📋 Planlanan
- [ ] Mobil uygulama (React Native)
- [ ] Trafik verisi entegrasyonu
- [ ] Hava durumu etkisi hesaplaması
- [ ] Çok dilli destek genişletmesi

---

## 🔧 Yapılandırma

### Ortam Değişkenleri

| Değişken | Açıklama | Örnek |
|----------|----------|-------|
| `OPENAI_API_KEY` | OpenAI veya OpenRouter API anahtarı | `sk-...` |
| `OPENAI_BASE_URL` | API base URL (OpenRouter için) | `https://openrouter.ai/api/v1` |
| `OPENAI_MODEL` | Kullanılacak model | `gpt-4o-mini` |
| `DATABASE_URL` | PostgreSQL bağlantı string'i | `postgresql+asyncpg://...` |
| `REDIS_URL` | Redis bağlantı URL'i | `redis://localhost:6379` |
| `ALLOWED_ORIGINS` | CORS izinli origin'ler | `http://localhost:5173` |

---

## 🤝 Katkıda Bulunma

1. Fork yapın
2. Feature branch oluşturun (`git checkout -b feature/amazing-feature`)
3. Değişikliklerinizi commit edin (`git commit -m 'Add amazing feature'`)
4. Branch'i push edin (`git push origin feature/amazing-feature`)
5. Pull Request açın

---

## 📄 Lisans

Bu proje MIT Lisansı altında lisanslanmıştır. Detaylar için [LICENSE](LICENSE) dosyasına bakın.

---

## 📞 İletişim

Sorularınız için issue açabilir veya pull request gönderebilirsiniz.

---

<div align="center">
  <sub>Built with ❤️ for the EV community in Turkey</sub>
</div>