# Font Awesome Kullanım Kılavuzu

Font Awesome 6 artık projeye entegre edildi! İşte kullanım örnekleri:

## 🎯 Temel Kullanım

### HTML içinde:
```html
<i class="fa-solid fa-bolt"></i> Enerji
<i class="fa-solid fa-chart-line"></i> Analiz
<i class="fa-solid fa-leaf"></i> Sürdürülebilirlik
```

### Streamlit markdown içinde:
```python
st.markdown("""
    <div>
        <i class="fa-solid fa-bolt" style="color: #10b981;"></i>
        <span>Enerji Tüketimi</span>
    </div>
""", unsafe_allow_html=True)
```

## 📦 Önerilen İkonlar (Enerji Teması)

### Enerji & Güç
- `fa-bolt` - Elektrik/Enerji
- `fa-plug` - Elektrik Fişi
- `fa-battery-full` - Batarya
- `fa-solar-panel` - Güneş Paneli
- `fa-wind` - Rüzgar Enerjisi

### Analiz & Grafikler
- `fa-chart-line` - Çizgi Grafik
- `fa-chart-bar` - Bar Grafik
- `fa-chart-pie` - Pasta Grafik
- `fa-chart-area` - Alan Grafik
- `fa-magnifying-glass-chart` - Analiz

### Çevre & Sürdürülebilirlik
- `fa-leaf` - Yaprak/Yeşil
- `fa-seedling` - Fidan
- `fa-earth-americas` - Dünya
- `fa-recycle` - Geri Dönüşüm
- `fa-tree` - Ağaç

### Veri & Bilgi
- `fa-database` - Veritabanı
- `fa-server` - Sunucu
- `fa-cloud` - Bulut
- `fa-download` - İndirme
- `fa-upload` - Yükleme

### Kullanıcı & Sistem
- `fa-user` - Kullanıcı
- `fa-gear` - Ayarlar
- `fa-bell` - Bildirim
- `fa-circle-info` - Bilgi
- `fa-circle-check` - Onay

### Zaman & Takvim
- `fa-clock` - Saat
- `fa-calendar` - Takvim
- `fa-hourglass` - Kum Saati
- `fa-stopwatch` - Kronometre

## 🎨 Stil Örnekleri

### Renkli İkon
```html
<i class="fa-solid fa-bolt" style="color: #10b981; font-size: 1.5rem;"></i>
```

### Gradient İkon
```html
<i class="fa-solid fa-leaf" style="
    background: linear-gradient(135deg, #10b981 0%, #059669 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    font-size: 2rem;
"></i>
```

### Animasyonlu İkon
```html
<i class="fa-solid fa-spinner fa-spin" style="color: #0071e3;"></i>
<i class="fa-solid fa-heart fa-beat" style="color: #ef4444;"></i>
```

## 💡 Kullanım Yerleri

1. **Metrik Kartları**: Her metriğin yanına ilgili ikon
2. **Başlıklar**: Bölüm başlıklarında görsel vurgu
3. **Butonlar**: Aksiyon butonlarında açıklayıcı ikonlar
4. **Bilgi Kutuları**: st.info, st.warning için özel ikonlar
5. **Menü Öğeleri**: Navigasyon için

## 🔗 Kaynaklar

- Font Awesome Arama: https://fontawesome.com/search
- Tüm İkonlar: https://fontawesome.com/icons
- Animasyonlar: https://fontawesome.com/docs/web/style/animate
