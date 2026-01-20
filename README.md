# GitLab DORA Metrics Collector

GitLab'dan ekip ve kişi bazında DORA metriklerini toplamak için Python aracı.

## DORA Metrikleri

Bu araç aşağıdaki DORA metriklerini toplar:

1. **Deployment Frequency** - Dağıtım sıklığı
2. **Lead Time for Changes** - Değişiklik için teslim süresi
3. **Time to Restore Service** - Hizmet geri yükleme süresi
4. **Change Failure Rate** - Değişiklik başarısızlık oranı

## Gereksinimler

- Python 3.8+
- GitLab instance erişimi
- Personal Access Token (API yetkisi ile)

## Kurulum

### 1. Bağımlılıkları Yükleyin

```bash
# Virtual environment oluşturun (önerilen)
python3 -m venv venv
source venv/bin/activate

# Bağımlılıkları yükleyin
pip install -r requirements.txt
```

### 2. GitLab Kaynaklarını Keşfedin

Token'ınızı `.env` dosyasına ekledikten sonra, önce erişiminiz olan tüm grupları ve projeleri listeleyin:

```bash
python3 gitlab_discover.py
```

Bu script:
- Tüm erişilebilir GitLab gruplarını listeler
- Tüm projelerinizi gösterir
- Grup ID'lerini ve Proje ID'lerini verir
- `.env` dosyanız için öneriler sunar

### 3. Yapılandırma

`.env.example` dosyasını `.env` olarak kopyalayın ve bilgilerinizi girin:

```bash
cp .env.example .env
```

`.env` dosyasını düzenleyin:

```env
GITLAB_URL=https://gitlab.yourcompany.com
GITLAB_TOKEN=your_personal_access_token_here
START_DATE=2024-01-01
END_DATE=2024-12-31
PROJECT_IDS=123,456,789
# VEYA
GROUP_ID=10
```

### 3. GitLab Personal Access Token Oluşturma

1. GitLab'da: **User Settings** → **Access Tokens**
2. Token adı: `DORA Metrics`
3. Seçilecek yetkiler:
   - `api` (API'ye tam erişim)
   - `read_api` (sadece okuma için)
4. **Create personal access token** butonuna tıklayın
5. Token'ı kopyalayın ve `.env` dosyasına ekleyin

## Kullanım

### Temel Kullanım

```bash
python gitlab_dora_metrics.py
```

### Çıktılar

Script çalıştırıldığında şu dosyaları oluşturur:

1. **gitlab_merge_requests_YYYYMMDD_HHMMSS.csv**
   - Tüm merge request detayları
   - Lead time hesaplamaları

2. **gitlab_user_stats_YYYYMMDD_HHMMSS.csv**
   - Kullanıcı bazında özet istatistikler
   - Ortalama/medyan lead time değerleri

3. **gitlab_dora_metrics_YYYYMMDD_HHMMSS.xlsx**
   - Tüm verileri içeren Excel dosyası
   - Ayrı sheet'lerde MR'lar ve kullanıcı istatistikleri

4. **gitlab_dora_raw_YYYYMMDD_HHMMSS.json** (GitLab Ultimate varsa)
   - API'den gelen ham DORA metrikleri

## Özellikler

### Ekip Bazında Metrikler

Bir GitLab grubundaki tüm projeleri analiz etmek için:

```env
GROUP_ID=10
```

### Kişi Bazında Metrikler

Script otomatik olarak her kullanıcı için:
- Toplam merge request sayısı
- Ortalama lead time
- Medyan lead time
- Min/Max lead time

hesaplar.

### Proje Bazında Metrikler

Belirli projeleri analiz etmek için:

```env
PROJECT_IDS=123,456,789
```

## Önemli Notlar

### GitLab Lisansları

- **DORA API**: GitLab **Ultimate** lisansı gerektirir
- **Alternatif Yöntem**: Script, Ultimate lisansı olmasa bile MR verilerinden lead time hesaplar

### API Rate Limiting

GitLab API rate limit'lerine dikkat edin:
- GitLab.com: 300 request/dakika (authenticated user)
- Self-hosted: Konfigürasyona göre değişir

## Troubleshooting

### "DORA metrics not available" Hatası

Bu hata GitLab Ultimate lisansınız yoksa normaldir. Script otomatik olarak alternatif yönteme geçer ve MR verilerinden metrik hesaplar.

### Token Yetki Hatası

Personal Access Token'ın `api` yetkisine sahip olduğundan emin olun.

### Proje Bulunamadı

Project ID'lerinin doğru olduğunu kontrol edin. GitLab'da proje settings sayfasından ID'yi görebilirsiniz.

## Örnek Çıktılar

### Konsol Çıktısı

```
============================================================
Processing project 123
============================================================
Fetching deployment_frequency for project 123...
Fetching lead_time_for_changes for project 123...
Fetching merge requests for project 123...

============================================================
Summary Statistics by User
============================================================
author          author_name     total_mrs  avg_lead_time_hours  median_lead_time_hours
john.doe        John Doe        45         12.5                 10.2
jane.smith      Jane Smith      38         15.3                 14.1
```

### CSV Çıktısı

CSV dosyaları Excel, Google Sheets veya herhangi bir veri analiz aracında açılabilir.

## Gelişmiş Kullanım

### Custom Analysis

Script'i Python kodunuzda kullanabilirsiniz:

```python
from gitlab_dora_metrics import GitLabDORAMetrics

collector = GitLabDORAMetrics(
    gitlab_url='https://gitlab.yourcompany.com',
    token='your_token'
)

# Belirli bir proje için DORA metrikleri
metrics = collector.get_all_dora_metrics(
    project_id=123,
    start_date='2024-01-01',
    end_date='2024-12-31'
)

# Merge request analizi
mr_df = collector.get_merge_requests_by_user(
    project_id=123,
    start_date='2024-01-01',
    end_date='2024-12-31'
)
```

## Katkıda Bulunma

İyileştirme önerileri ve hata bildirimleri için issue açabilirsiniz.

## Lisans

MIT
