➤ Demo Videosu : [`Syntax Highlighter`](https://youtu.be/pwqJkFLGk84)

# Gerçek Zamanlı Python Sözdizimi Vurgulayıcı  
**BLM0238 Programlama Dilleri Projesi**

Python ve Tkinter kullanılarak oluşturulmuş, sözcüksel analiz ve ayrıştırma yeteneklerine sahip gerçek zamanlı bir sözdizimi vurgulayıcısı uygulaması.

---

## 🎯 Projeye Genel Bakış
Bu proje, Python kaynak kodunun gerçek zamanlı analizini gerçekleştiren kapsamlı bir sözdizimi vurgulayıcı uygular:

- **Lexical Analiz**: Durum makinesi tabanlı tokenizasyon 
- **Sözdizimsel Analiz**: Top-down özyinelemeli iniş ayrıştırma
- **Gerçek Zamanlı GUI**: Etkileşimli sözdizimi vurgulama arayüzü  
- **Token Analizi**: Detaylı token incelemesi ve istatistikleri 
- **Hata Tespiti**: Ayrıştırma hatası raporlama ve kurtarma

---

## 🏗️ Mimari
Proje beş ana bileşen halinde modülerleştirilmiştir:

### Modüller
- `tokens.py` - Belirteç türü tanımları ve veri yapıları  
- `lexer.py` - Sonlu durum makinesi ile sözcük çözümleyici   
- `parser.py` - Özyinelemeli iniş ayrıştırıcı uygulaması  
- `gui.py` - GUI bileşenleri ve sözdizimi vurgulama mantığı  
- `main.py` - Uygulama giriş noktası ve sistem kontrolleri

---

## 🚀 Özellikler

### Lexical Analiz
- **Durum Makinesi Uygulaması**: Tokenleştirme için sonlu durum otomatı 
- **Token Türleri**: Anahtar kelimeler, operatörler, dizeler vb. dahil olmak üzere 10 farklı belirteç kategorisi  
- **Hata İşleme**: Hatalı biçimlendirilmiş girdilerin sağlam bir şekilde işlenmesi 
- **Pozisyon Takibi**: Her bir belirteç için satır ve sütun bilgileri  

### Ayrıştırma
- **LL(1) Parser**: Top-down özyinelemeli iniş uygulaması  
- **Hata Kurtarma**: Ayrıştırma hatalarından sonra senkronizasyon  
- **Python Yapıları**: Fonksiyonları, döngüleri, koşulluları, ifadeleri destekler

### GUI Arayüzü
- **Gerçek Zamanlı Vurgulama**: 300ms debounced güncellemeleri  
- **Bölmeli bölme Düzenleyici**: Girdi ve vurgulanan çıktı yan yana  
- **Sekmeli Arayüz**: Düzenleme, analiz ve istatistikler için ayrı görünümler  
- **Token Analizi**: Tüm belirteçleri ayrıntılarıyla birlikte gösteren etkileşimli tablo  
- **İstatistik Paneli**: Kapsamlı analiz metrikleri

---

## 📋 Gereksinimler
- Python 3.7+
- `tkinter` (çoğu Python kurulumuyla birlikte gelir)
- Harici bağımlılık gerektirmez

---

## 🏃‍♂️ Hızlı Başlangıç

### 1. Proje Dosyalarını İndir
Tüm dosyaların aynı dizinde olduğundan emin olun:

```
project/
├── main.py          # Ana uygulama giriş noktası
├── tokens.py        # Belirteç tanımları
├── lexer.py         # Sözcük çözümleyici
├── parser.py        # Ayrıştırıcı uygulaması
├── gui.py           # GUI bileşenleri
└── README.md        
```

### 2. Uygulamayı Çalıştırın
```bash
# Temel Kullanım
python main.py

# Sistem testleri ile çalıştır
python main.py --test

# Yardım bilgilerini göster
python main.py --help
```

### 3. Arayüz Kullanımı

**Kod Düzenleyici Sekmesi:**
- Python kodunu sol panele yazın veya yapıştırın  
- Sağ panelde sözdizimi vurgulanmış çıktıyı görüntüleme  
- Siz yazdıkça renkler otomatik olarak güncellenir  

**Token Analizi Sekmesi:**
- Konum, tür ve değer ile tüm belirteçlere göz atın  
- Tokenleştirme sonuçlarını ayrıntılı olarak inceleyin  

**İstatistik Sekmesi:**
- Jeton dağılımını ve sayılarını görüntüleyin  
- Ayrıştırma hatalarını ve uyarılarını kontrol edin   

---

## 🎨 Renk Şeması

| Token Type   | Color       | Hex      |
|--------------|-------------|----------|
| Keywords     | Mavi        |🟦 #0066CC  |
| Strings      | Yeşil       |🟩 #009900  |
| Numbers      | Turuncu     |🟧 #FF6600  |
| Comments     | Gri         |⬜️ #808080  |
| Operators    | Kırmızı     |🟥 #CC0000  |
| Delimiters   | Mor         |🟪 #663399  |
| Identifiers  | Siyah       |⬛ #000000  |
| Errors       | Parlak Kırmızı|🔴 #FF0000  |

---

## 🔧 Teknik Uygulama

### Sözcüksel Analiz Yöntemi
- **Durum Diyagramı Uygulaması**: Her karakter durum geçişlerini tetikler  
- **Sonsuz Durum Makinesi**: Karmaşık tokenizasyon kurallarını işler  

### Ayrıştırıcı Yöntemi
- **Top-Down Yaklaşımı**: LL(1) özellikleri ile özyinelemeli iniş  
- **Hata Kurtarma**: Sağlam ayrıştırma için senkronizasyon noktaları  

### Gerçek Zamanlı İşleme
- **İptal Edilen Güncellemeler**: 300ms gecikme aşırı işlemeyi önler  
- **Eklemeli Analiz**: Metin değişikliklerinde verimli yeniden analiz  
- **Engellemeyen kullanıcı arayüzü**: Analiz sırasında duyarlı arayüzü korur

---

## 📊 Örnek Analiz Çıktısı

```
=== LEXICAL ANALYSIS STATISTICS ===

Total Tokens: 156
Total Lines: 23

Token Type Distribution:
------------------------------
WHITESPACE     :     45 ( 28.8%)
IDENTIFIER     :     32 ( 20.5%)
DELIMITER      :     28 ( 17.9%)
KEYWORD        :     18 ( 11.5%)
NEWLINE        :     15 (  9.6%)
STRING         :      8 (  5.1%)
OPERATOR       :      6 (  3.8%)
NUMBER         :      3 (  1.9%)
COMMENT        :      1 (  0.6%)
```

---

## 🧪 Test

Uygulama yerleşik modül testi içerir:

```bash
# Sistem testlerini çalıştırın
python main.py --test
```

Bunlar doğrulanır:

✅ Tüm modüller doğru şekilde içe aktarılır  
✅ Temel sözcüksel analiz işlevi  
✅ Ayrıştırıcı başlatma ve temel ayrıştırma  
✅ GUI modülü kullanılabilirliği  
✅ Sistem gereksinimleri (Python sürümü, tkinter)

---

## 🏆 Proje Şartnamesi Karşılandı

### Akademik Gereklilikler
✅ Hedef Dil: Python sözdizimi vurgulama  
✅ Uygulama Dili: Tkinter ile Python  
✅ Sözcüksel Yöntem: Durum diyagramı ve program uygulaması  
✅ Ayrıştırıcı Yöntemi: Yukarıdan aşağıya özyinelemeli iniş  
✅ Gerçek Zamanlı İşleme: Anında sözdizimi vurgulama  
✅ GUI Arayüzü: Eksiksiz Tkinter tabanlı arayüz

### Teknik Başarılar
✅ Modüler Tasarım: Endişelerin temiz bir şekilde ayrılması  
✅ Hata İşleme: Sağlam hata algılama ve kurtarma  
✅ Performans: Verimli gerçek zamanlı analiz  
✅ Kullanılabilirlik: Sezgisel ve duyarlı arayüz  
✅ Dokümantasyon: Kapsamlı kod dokümantasyonu

---

## 📝 Geliştirme Notları

### Eklenti Olanakları
- Çoklu dil desteği (Java, C++, vb.)
- Gelişmiş ayrıştırma (tam Python grameri)
- Kod tamamlama önerileri
- Vurgulanan kodu dışa aktarma (HTML, PDF)
- Özel temalar için eklenti mimarisi

### Performans Hususları
- Token analizi, görüntüleme performansı için 500 token ile sınırlıdır
- Debounced güncellemeleri aşırı işlemeyi önler
- Sözcüksel analizde verimli dizgi işleme
