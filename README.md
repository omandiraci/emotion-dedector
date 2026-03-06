# 🎭 Emotion Detector

Gerçek zamanlı yüz duygu analizi uygulaması. Kameradan aldığı görüntüdeki yüzleri tespit eder ve 7 farklı duyguyu analiz ederek ekranda gösterir.

## 🎯 Özellikler

- Gerçek zamanlı yüz tespiti
- 7 farklı duygu analizi (Mutlu, Kızgın, Üzgün, Şaşkın, Korku, İğrenme, Nötr)
- Her yüzün yanında dominant duygu ve yüzde gösterimi
- Duygu dağılımı bar chart görselleştirmesi
- Performans optimizasyonu (her 3 frame'de bir analiz)
- Türkçe arayüz

## 🛠 Kullanılan Teknolojiler

| Teknoloji | Kullanım Amacı |
|---|---|
| Python 3.13 | Ana programlama dili |
| OpenCV | Kamera erişimi, yüz tespiti (Haar Cascade), görüntü işleme |
| TensorFlow / Keras | Duygu analizi modeli (mini XCEPTION CNN) |
| NumPy | Görüntü verisi işleme |

## 📊 Desteklenen Duygular

| Duygu | Renk |
|---|---|
| Mutlu | 🟢 Yeşil |
| Kızgın | 🔴 Kırmızı |
| Üzgün | 🔵 Mavi |
| Şaşkın | 🟡 Sarı |
| Korku | 🟣 Mor |
| İğrenme | 🟢 Koyu Yeşil |
| Nötr | ⚪ Gri |

## 🚀 Hızlı Başlangıç

```bash
# Projeyi klonla
git clone https://github.com/KULLANICI_ADIN/emotion-detector.git
cd emotion-detector

# Sanal ortam oluştur ve aktif et
python3.13 -m venv .venv
source .venv/bin/activate

# Bağımlılıkları kur
pip install opencv-python tensorflow numpy

# Çalıştır
python emotion_detector.py
```

## ⌨️ Kontroller

| Tuş | İşlev |
|---|---|
| `q` | Uygulamayı kapat |
| `Ctrl + C` | Terminal'den durdur |

## 📁 Proje Yapısı

```
emotion-detector/
├── emotion_detector.py   # Ana uygulama
├── models/               # İndirilen model dosyaları (otomatik)
├── .gitignore
├── README.md
└── ADMIN_GUIDE.md
```

## 📝 Notlar

- İlk çalıştırmada duygu analizi modeli (~870KB) otomatik indirilir
- macOS'ta kamera izni gereklidir (System Settings → Privacy & Security → Camera)
- Birden fazla kamera varsa `cv2.VideoCapture(0)` içindeki index değiştirilebilir

## 📄 Lisans

MIT
