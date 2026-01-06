# Şarj İstasyonları Veri Seti

Bu dokümant, EV AI Navigation System'da kullanılan şarj istasyonu verilerini açıklar.

## 📊 Veri Seti Özeti

| Özellik | Değer |
|---------|-------|
| Toplam İstasyon | 286 |
| Kapsanan Şehir | 26 |
| Şarj Ağı Sayısı | 7 |
| Güç Aralığı | 50 - 350 kW |
| Veri Formatı | CSV |

---

## 📍 Şehir Dağılımı

| Şehir | İstasyon Sayısı | Açıklama |
|-------|-----------------|----------|
| İstanbul | 50+ | En yoğun kapsama, Avrupa ve Anadolu yakası |
| Ankara | 32+ | Başkent, merkez ilçeler ve bağlantı yolları |
| İzmir | 25+ | Ege bölgesi merkezi, sahil şeridi |
| Antalya | 20+ | Turizm bölgeleri ve oteller |
| Bursa | 15+ | Sanayi bölgeleri ve şehir merkezi |
| Adana | 15+ | Güney Anadolu merkezi |
| Gaziantep | 12+ | Güneydoğu bölgesi |
| Konya | 12+ | İç Anadolu |
| Diğer | 100+ | Trabzon, Erzurum, Samsun, Van, vb. |

---

## ⚡ Şarj Ağları

### 1. Sharz
- **Kapsam**: Türkiye geneli en yaygın ağ
- **Güç**: 50-180 kW
- **Konektör**: CCS2, Type 2
- **Özellik**: AVM'ler ve şehir merkezlerinde yoğun

### 2. GoCharge
- **Kapsam**: Büyük şehirler ve otoyollar
- **Güç**: 100-250 kW
- **Konektör**: CCS2
- **Özellik**: Havalimanları ve ana arterler

### 3. Eşarj (Enerjisa)
- **Kapsam**: Türkiye geneli
- **Güç**: 50-150 kW
- **Konektör**: CCS2, CHAdeMO
- **Özellik**: Şehir merkezleri ve konut alanları

### 4. Voltrun
- **Kapsam**: Büyüyen yerli ağ
- **Güç**: 50-150 kW
- **Konektör**: CCS2
- **Özellik**: İlçe merkezleri ve ara bölgeler

### 5. ZES (Zorlu Energy Solutions)
- **Kapsam**: Premium lokasyonlar
- **Güç**: 100-180 kW
- **Konektör**: CCS2
- **Özellik**: Zorlu Center, lüks AVM'ler

### 6. Tesla Supercharger
- **Kapsam**: Seçili konumlar
- **Güç**: 250 kW
- **Konektör**: Tesla, CCS2 (adapter ile)
- **Özellik**: En hızlı şarj, Tesla araçlarına öncelik

### 7. Aytemiz Electra
- **Kapsam**: Otoyol dinlenme tesisleri
- **Güç**: 180 kW
- **Konektör**: CCS2
- **Özellik**: Petrol istasyonu entegrasyonu

---

## 🔌 Güç Seviyeleri

| Kategori | Güç (kW) | Şarj Süresi (20-80%) | Kullanım Alanı |
|----------|----------|----------------------|----------------|
| Normal | 50 | ~60 dakika | Şehir içi, alışveriş |
| Hızlı | 100-150 | ~30-40 dakika | Orta mesafe |
| Ultra Hızlı | 180-250 | ~15-25 dakika | Otoyol, uzun mesafe |
| Süper Hızlı | 350 | ~10-15 dakika | Tesla Supercharger |

---

## 📁 CSV Formatı

### Dosya Konumu
```
data/charging_stations/charging_stations_map.csv
```

### Sütunlar

| Sütun | Tip | Açıklama |
|-------|-----|----------|
| `Şarj İstasyonu` | string | İstasyon adı |
| `Şehir` | string | Şehir adı (büyük harf) |
| `Latitude` | float | Enlem koordinatı |
| `Longitude` | float | Boylam koordinatı |
| `last_updated` | date | Son güncelleme tarihi |
| `next_update` | date | Sonraki güncelleme tarihi |
| `estimated_current_kW` | int | Şarj gücü (kW) |
| `cluster` | int | Bölge kümesi (0-4) |

### Örnek Satır
```csv
Sharz İstinyePark AVM,İSTANBUL,41.1088,29.0223,2025-03-17,2025-04-16,180,3
```

---

## 🗺️ Konum Tipleri

### AVM'ler
- İstinyePark, Zorlu Center, Cevahir, Forum, Optimum, Mall of İstanbul
- Konum: Şehir merkezleri
- Güç: 100-180 kW
- Avantaj: Alışveriş sırasında şarj

### Havalimanları
- İstanbul, Sabiha Gökçen, Esenboğa, Adnan Menderes
- Güç: 250 kW
- Avantaj: Uzun park süreleri

### Otoyollar
- TEM, E5, D100, O-4 bağlantıları
- Aytemiz Electra ağı
- Güç: 180 kW
- Avantaj: Hızlı şarj, kolay erişim

### Oteller
- 5 yıldızlı oteller, resort'lar
- Konum: Turizm bölgeleri (Antalya, Muğla)
- Güç: 50-150 kW
- Avantaj: Konaklama sırasında şarj

### Şehir Merkezleri
- Ana caddeler, meydanlar
- Güç: 50-100 kW
- Avantaj: Günlük kullanım

---

## 🔧 Veri Güncelleme

### Manuel Güncelleme
CSV dosyasını düzenleyerek yeni istasyon ekleyebilirsiniz:

```csv
Yeni İstasyon Adı,ŞEHİR,41.0000,29.0000,2025-01-06,2025-02-06,150,3
```

### Otomatik Yeniden Yükleme
Backend yeniden başlatıldığında CSV otomatik yüklenir:

```bash
# Backend'i yeniden başlat
cd backend
uvicorn orchestrator:app --reload
```

---

## 📈 Gelecek Planları

- [ ] Gerçek zamanlı müsaitlik entegrasyonu
- [ ] Kullanıcı yorumları ve puanlama
- [ ] Fotoğraf desteği
- [ ] Fiyat karşılaştırma
- [ ] Rezervasyon sistemi
