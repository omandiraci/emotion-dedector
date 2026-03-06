# 🔧 Admin Guide - Emotion Detector

Bu doküman uygulamanın kurulumu, yapılandırması ve sorun giderme adımlarını içerir.

---

## 1. Sistem Gereksinimleri

| Gereksinim | Minimum |
|---|---|
| Python | 3.10+ (önerilen: 3.13) |
| RAM | 4 GB |
| Kamera | Dahili veya harici webcam |
| İşletim Sistemi | macOS, Linux, Windows |
| Disk | ~500 MB (model + kütüphaneler) |

---

## 2. Kurulum

### 2.1 Python Kontrolü

```bash
python3 --version
```

Python 3.10 veya üzeri gereklidir.

### 2.2 Sanal Ortam Oluşturma

```bash
python3.13 -m venv .venv
source .venv/bin/activate        # macOS / Linux
# .venv\Scripts\activate         # Windows
```

### 2.3 Bağımlılıkları Kurma

```bash
pip install opencv-python tensorflow numpy
```

### 2.4 Model Dosyası

İlk çalıştırmada `fer2013_mini_XCEPTION` modeli otomatik indirilir:
- Kaynak: https://github.com/oarriaga/face_classification
- Boyut: ~870 KB
- Konum: `./models/` klasörü

---

## 3. Yapılandırma

### 3.1 Kamera Seçimi

Birden fazla kamera varsa `emotion_detector.py` dosyasında:

```python
cap = cv2.VideoCapture(0)   # 0 = varsayılan kamera
cap = cv2.VideoCapture(1)   # 1 = ikinci kamera
```

Mevcut kameraları listelemek için:

```python
import cv2
for i in range(5):
    cap = cv2.VideoCapture(i)
    if cap.isOpened():
        print(f"Kamera {i}: aktif")
        cap.release()
```

### 3.2 Performans Ayarı

Analiz sıklığını değiştirmek için `frame_count % 3` değerini düzenle:

```python
if frame_count % 3 == 0:    # Her 3 frame'de bir (varsayılan)
if frame_count % 1 == 0:    # Her frame (yavaş ama hassas)
if frame_count % 10 == 0:   # Her 10 frame'de bir (hızlı ama gecikmeli)
```

### 3.3 Yüz Tespiti Hassasiyeti

```python
faces = face_cascade.detectMultiScale(gray, 1.3, 5, minSize=(48, 48))
#                                           │    │           │
#                                           │    │           └─ Minimum yüz boyutu (piksel)
#                                           │    └─ minNeighbors (yüksek = daha az false positive)
#                                           └─ scaleFactor (düşük = daha hassas ama yavaş)
```

---

## 4. macOS Kamera İzni

1. **System Settings** → **Privacy & Security** → **Camera**
2. Terminal uygulamanız için izni açın
3. Terminal'i yeniden başlatın

---

## 5. Sorun Giderme

### Kamera açılmıyor

```
OpenCV: not authorized to capture video (status 0)
```
**Çözüm:** macOS kamera izni ver (Bölüm 4)

### Model indirme hatası

```
ConnectionError: Unable to download model
```
**Çözüm:** İnternet bağlantısını kontrol et. Manuel indirmek için:
```bash
mkdir -p models
curl -L -o models/emotion_model.hdf5 https://github.com/oarriaga/face_classification/raw/master/trained_models/emotion_models/fer2013_mini_XCEPTION.102-0.66.hdf5
```

### Yüz tespit edilmiyor

- Kameranın önünde yeterli ışık olduğundan emin ol
- Yüzün kameraya dönük olmalı
- `minSize` değerini düşür: `minSize=(30, 30)`

### Uygulama yavaş çalışıyor

- `frame_count % 3` değerini artır (örn: `% 10`)
- Kamera çözünürlüğünü düşür:
```python
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
```

---

## 6. Mimari

```
Kamera (OpenCV)
    │
    ▼
Frame Yakalama
    │
    ▼
Gri Tonlama (cv2.cvtColor)
    │
    ▼
Yüz Tespiti (Haar Cascade)
    │
    ▼
ROI Çıkarma + 64x64 Resize
    │
    ▼
Duygu Modeli (mini XCEPTION CNN)
    │
    ▼
7 Duygu Olasılığı
    │
    ▼
Ekranda Gösterim (OpenCV)
```

---

## 7. Model Bilgisi

- **Model:** mini XCEPTION
- **Eğitim Verisi:** FER2013 (35.887 yüz görüntüsü)
- **Doğruluk:** ~%66 (test seti)
- **Giriş:** 64x64 gri tonlama görüntü
- **Çıkış:** 7 duygu olasılığı
