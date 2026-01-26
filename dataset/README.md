# Performance Dataset

Bu klasör, Odeal performans değerlendirmeleri için GitLab ve Jira API'lerinden çekilen ham ve işlenmiş verileri içerir.

---

## 📁 Klasör Yapısı

```
dataset/
├── README.md           # Bu dosya
├── raw/                # API'lerden çekilen ham veriler
│   ├── gitlab/         # GitLab API verileri
│   └── jira/           # Jira API verileri
└── processed/          # İşlenmiş ve analiz edilmiş veriler
```

---

## 🔄 Veri Toplama

### GitLab Verileri

GitLab API'den veri çekmek için:

```bash
cd ../scripts/gitlab/
python gitlab_dora_metrics.py
```

**Çıktı Konumu:** `dataset/raw/gitlab/`

**İçerik:**
- Merge requests
- Commits
- DORA metrikleri
- User statistics

---

### Jira Verileri

Jira API'den veri çekmek için:

```bash
cd ../scripts/jira/
python jira_team_analysis.py
```

**Çıktı Konumu:** `dataset/raw/jira/`

**İçerik:**
- Issue listesi
- Sprint verileri
- User workload
- Project insights

---

## 📊 Veri İşleme

Ham veriler toplandıktan sonra, analiz scriptleri ile işlenir:

```bash
cd ../scripts/
python generate_comprehensive_report.py
```

**Çıktı Konumu:** `dataset/processed/`

---

## ⚙️ Konfigürasyon

Veri çekmeden önce `.env` dosyasını yapılandırın:

```env
# GitLab
GITLAB_URL=https://gitlab.yourcompany.com
GITLAB_TOKEN=your_token

# Jira
JIRA_URL=https://yourcompany.atlassian.net
JIRA_USERNAME=your_email
JIRA_API_TOKEN=your_token

# Tarih Aralığı
START_DATE=2025-01-01
END_DATE=2025-12-31
```

---

## 📝 Veri Formatları

### GitLab CSV Formatı
- `gitlab_merge_requests_YYYYMMDD_HHMMSS.csv`
- `gitlab_user_stats_YYYYMMDD_HHMMSS.csv`
- `gitlab_dora_metrics_YYYYMMDD_HHMMSS.xlsx`

### Jira CSV Formatı
- `jira_team_analysis_YYYYMMDD_HHMMSS.csv`
- `jira_user_workload_YYYYMMDD_HHMMSS.xlsx`

---

## 🗑️ Temizlik

Eski verileri temizlemek için:

```bash
# Ham verileri temizle
rm -rf dataset/raw/gitlab/* dataset/raw/jira/*

# İşlenmiş verileri temizle
rm -rf dataset/processed/*
```

---

*Son güncelleme: 2026-01-22*
