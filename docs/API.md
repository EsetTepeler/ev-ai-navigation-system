# API Dokümantasyonu

Bu dokümant, EV AI Navigation System API endpointlerinin detaylı açıklamasını içerir.

## 📌 Temel Bilgiler

| Özellik | Değer |
|---------|-------|
| Base URL | `http://localhost:8000` |
| API Versiyonu | 2.0 |
| Format | JSON |
| Encoding | UTF-8 |

## 🔐 Authentication

Şu anda API public erişime açıktır. Gelecekte JWT tabanlı authentication eklenecektir.

---

## 📡 Endpoints

### Sistem Endpoints

#### `GET /`
Sistem durumu ve versiyon bilgisi.

**Response:**
```json
{
  "name": " EV Navigation API",
  "version": "2.0",
  "status": "active"
}
```

---

#### `GET /api/test-db`
PostgreSQL veritabanı bağlantı durumu.

**Response (Success):**
```json
{
  "status": "connected",
  "database": "ev_navigation",
  "stats": {
    "vehicles": 384,
    "charging_stations": 286
  }
}
```

**Response (Error):**
```json
{
  "error": "Database connection failed",
  "code": "DATABASE_ERROR",
  "details": {...}
}
```

---

#### `GET /api/redis-status`
Redis cache durumu.

**Response:**
```json
{
  "status": "connected",
  "cached_keys": 12
}
```

---

### Araç Endpoints

#### `GET /api/vehicles-db`
Tüm elektrikli araç modellerini listeler. Redis cache kullanır.

**Response:**
```json
{
  "vehicles": [
    {
      "model_id": "tesla_model_3_lr",
      "manufacturer": "Tesla",
      "model_name": "Model 3 Long Range",
      "year": 2024,
      "category": "Sedan",
      "battery_capacity_kwh": 82.0,
      "epa_range_km": 602,
      "energy_consumption_kwh_per_100km": 14.1,
      "max_charging_power_kw": 250,
      "supported_connectors": ["Tesla", "CCS2"]
    }
  ],
  "total": 384
}
```

---

#### `POST /api/smart-vehicle-search`
AI destekli akıllı araç araması. Doğal dil sorguları destekler.

**Request Body:**
```json
{
  "query": "500 km üzeri menzilli, hızlı şarj destekli SUV"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "model_id": "bmw_ix_xdrive50",
      "manufacturer": "BMW",
      "model_name": "iX xDrive50",
      "match_score": 0.95,
      "match_reasons": [
        "630 km menzil",
        "200 kW DC şarj desteği",
        "SUV kategorisi"
      ]
    }
  ],
  "query_analysis": {
    "range_requirement": "500+ km",
    "body_type": "SUV",
    "charging_preference": "fast"
  }
}
```

---

### Şarj İstasyonu Endpoints

#### `GET /api/charging/stations`
Şarj istasyonlarını listeler. Çeşitli filtreleme seçenekleri sunar.

**Query Parameters:**

| Parametre | Tip | Zorunlu | Açıklama |
|-----------|-----|---------|----------|
| `city` | string | Hayır | Şehir adı (büyük harf, örn: `ANKARA`) |
| `lat` | float | Hayır | Enlem (yarıçap araması için) |
| `lon` | float | Hayır | Boylam (yarıçap araması için) |
| `radius` | float | Hayır | Kilometre cinsinden yarıçap (varsayılan: 100) |
| `min_power` | int | Hayır | Minimum güç (kW) |
| `max_power` | int | Hayır | Maksimum güç (kW) |

**Örnek İstekler:**

```bash
# Tüm istasyonlar
GET /api/charging/stations

# İstanbul'daki istasyonlar
GET /api/charging/stations?city=İSTANBUL

# Belirli konumdan 50km yarıçapta
GET /api/charging/stations?lat=41.0082&lon=28.9784&radius=50

# 150kW üzeri hızlı şarj istasyonları
GET /api/charging/stations?min_power=150
```

**Response:**
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
      "last_updated": "2025-03-17",
      "next_update": "2025-04-16",
      "cluster": 3,
      "connector_type": "DC Fast Charge (CCS)",
      "charging_speed": "Ultra Fast",
      "price_per_kwh": 0.45,
      "availability": "Available",
      "total_ports": 2,
      "available_ports": 1
    }
  ],
  "filter": {
    "type": "city",
    "value": "İSTANBUL"
  }
}
```

**Desteklenen Şehirler:**
- İSTANBUL (50+ istasyon)
- ANKARA (32+ istasyon)
- İZMİR (25+ istasyon)
- ANTALYA (20+ istasyon)
- BURSA, ADANA, GAZİANTEP, KONYA, TRABZON, KAYSERİ, SAMSUN, MALATYA, DENİZLİ, KOCAELİ, ESKİŞEHİR, BALIKESİR, MANİSA, MUĞLA, DİYARBAKIR, MERSİN, VAN, ERZURUM, ŞANLIURFA, OSMANİYE, SİVAS, SAKARYA, DÜZCE, NEVŞEHİR, ÇORUM

**Şarj Ağları:**
- Sharz
- GoCharge
- Eşarj
- Voltrun
- ZES (Zorlu Energy Solutions)
- Tesla Supercharger
- Aytemiz Electra

---

#### `GET /api/charging/networks`
Desteklenen şarj ağları hakkında bilgi.

**Response:**
```json
{
  "networks": [
    {
      "name": "Tesla Supercharger",
      "connector_types": ["Tesla", "CCS1"],
      "max_power_kw": 250,
      "coverage": "Extensive highway coverage",
      "membership_required": false,
      "pricing_model": "Per kWh"
    }
  ]
}
```

---

#### `GET /api/charging/connectors`
Şarj konnektör tipleri hakkında bilgi.

**Response:**
```json
{
  "connectors": [
    {
      "type": "CCS2",
      "name": "Combined Charging System (Europe)",
      "power_levels": ["Level 2 AC", "DC Fast Charging"],
      "max_power_kw": 350,
      "vehicles": ["BMW", "Mercedes", "Audi", "Volkswagen"]
    }
  ]
}
```

---

#### `GET /api/charging/pricing`
Şarj ağlarının fiyatlandırma bilgileri.

**Response:**
```json
{
  "pricing_comparison": [
    {
      "network": "Tesla Supercharger",
      "pricing_model": "Per kWh",
      "average_cost_per_kwh": 0.28,
      "peak_pricing": true,
      "idle_fees": "Yes, after charging complete"
    }
  ]
}
```

---

### Navigasyon Endpoints

#### `POST /api/navigation/simple-route`
Şarj duraklı rota hesaplama. Araç menzili ve batarya durumuna göre optimize eder.

**Request Body:**
```json
{
  "start_lat": 41.0082,
  "start_lon": 28.9784,
  "end_lat": 39.9334,
  "end_lon": 32.8597,
  "vehicle_range_km": 400,
  "battery_capacity_kwh": 75.0,
  "current_battery_percent": 80.0,
  "min_charge_percent": 20.0,
  "preferred_charge_percent": 80.0
}
```

**Parametreler:**

| Alan | Tip | Zorunlu | Açıklama |
|------|-----|---------|----------|
| `start_lat` | float | Evet | Başlangıç noktası enlem |
| `start_lon` | float | Evet | Başlangıç noktası boylam |
| `end_lat` | float | Evet | Bitiş noktası enlem |
| `end_lon` | float | Evet | Bitiş noktası boylam |
| `vehicle_range_km` | int | Evet | Araç maksimum menzili (km) |
| `battery_capacity_kwh` | float | Evet | Batarya kapasitesi (kWh) |
| `current_battery_percent` | float | Hayır | Mevcut batarya yüzdesi (varsayılan: 80) |
| `min_charge_percent` | float | Hayır | Minimum batarya yüzdesi (varsayılan: 20) |
| `preferred_charge_percent` | float | Hayır | Tercih edilen şarj yüzdesi (varsayılan: 80) |

**Response:**
```json
{
  "success": true,
  "route_coordinates": [
    [41.0082, 28.9784],
    [40.7322, 31.6089],
    [39.9334, 32.8597]
  ],
  "charging_stops": [
    {
      "station_id": "sharz_bolu_001",
      "name": "Sharz Bolu Otoyol",
      "latitude": 40.7322,
      "longitude": 31.6089,
      "power_kw": 180,
      "distance_from_start_km": 265.3,
      "charging_time_minutes": 35
    }
  ],
  "route_summary": {
    "total_distance_km": 453.2,
    "driving_time_minutes": 340,
    "charging_time_minutes": 35,
    "total_time_minutes": 375,
    "num_charging_stops": 1,
    "estimated_cost_tl": 45.80,
    "energy_needed_kwh": 85.2
  },
  "start_point": {
    "latitude": 41.0082,
    "longitude": 28.9784
  },
  "end_point": {
    "latitude": 39.9334,
    "longitude": 32.8597
  }
}
```

**Algoritma:**
1. Başlangıç ve bitiş arası toplam mesafe hesaplanır (Haversine)
2. Kullanılabilir menzil hesaplanır: `range × (current_percent - min_percent) / 100`
3. Rota koridorundaki (100km genişlik) istasyonlar filtrelenir
4. Menzil aşıldığında optimal şarj durağı seçilir
5. OSRM ile gerçek yol verisi alınır
6. Toplam süre ve maliyet hesaplanır

---

#### `POST /api/plan-route`
Basit rota planlama (şarj duraksız).

**Request Body:**
```json
{
  "start_location": "İstanbul",
  "destination": "Ankara",
  "vehicle_model": "tesla_model_3_lr"
}
```

**Response:**
```json
{
  "start": "İstanbul",
  "destination": "Ankara",
  "vehicle": "tesla_model_3_lr",
  "status": "calculated",
  "distance_km": 453.2,
  "time_minutes": 340
}
```

---

### AI Chat Endpoint

#### `POST /api/ai-chat`
AI destekli sohbet. Araç ve şarj istasyonu bağlamı ile zenginleştirilmiş yanıtlar.

**Request Body:**
```json
{
  "message": "İstanbul'dan Antalya'ya gideceksem hangi araç uygun olur?"
}
```

**Response:**
```json
{
  "response": "İstanbul'dan Antalya'ya giderken yaklaşık 700 km yol kat etmeniz gerekecek. Bu mesafe için şu araçları öneririm:\n\n1. **Tesla Model 3 Long Range** (602 km menzil) - 1 şarj durağı ile yeterli\n2. **BMW iX xDrive50** (630 km menzil) - Konforlu SUV seçeneği\n\nRota üzerinde Konya ve Isparta'da Sharz ve Eşarj istasyonları mevcut.",
  "context_used": {
    "vehicles_count": 384,
    "stations_count": 286
  }
}
```

---

## 🔴 Hata Kodları

| Kod | HTTP Status | Açıklama |
|-----|-------------|----------|
| `VALIDATION_ERROR` | 400 | Geçersiz istek parametreleri |
| `DATABASE_ERROR` | 500 | Veritabanı bağlantı hatası |
| `REDIS_ERROR` | 500 | Redis bağlantı hatası |
| `AI_SERVICE_ERROR` | 500 | OpenAI/OpenRouter hatası |
| `ROUTE_CALCULATION_ERROR` | 500 | Rota hesaplama hatası |
| `NOT_FOUND` | 404 | Kaynak bulunamadı |

**Hata Response Formatı:**
```json
{
  "error": "Error message",
  "code": "ERROR_CODE",
  "details": {
    "field": "additional info"
  },
  "timestamp": "2025-01-06T10:30:00Z"
}
```

---

## 📊 Rate Limiting

Şu anda rate limiting uygulanmamaktadır. Production ortamında:
- 100 request/dakika (AI endpoints)
- 1000 request/dakika (diğer endpoints)

---

## 🔧 CORS

Aşağıdaki origin'lere izin verilmektedir:
- `http://localhost:5173`
- `http://localhost:5174`
- `http://localhost:3000`
- `http://127.0.0.1:5173`
- `http://127.0.0.1:5174`

Diğer origin'ler için `.env` dosyasında `ALLOWED_ORIGINS` değişkenini güncelleyin.
