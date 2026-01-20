# Dataset - Supporting Data & Archives

Bu klasör, ana raporları destekleyen detaylı data ve eski raporları içerir.

**Ana raporlar için:** [../results/](../results/) klasörüne bakın.

---

## 📂 Klasör Yapısı

### 1. team-lead-analysis/

Her kişi için detaylı Excel ve CSV raporları.

```
team-lead-analysis/
├── team-lead-analysis-gokhan_ibrikci/
│   ├── team_lead_report_gokhan_ibrikci_*.xlsx
│   └── summary_gokhan_ibrikci_*.csv
│
├── team-lead-analysis-mert_kaim/
│   ├── team_lead_report_mert_kaim_*.xlsx
│   ├── summary_mert_kaim_*.csv
│   └── developer_health_score.csv
│
├── team-lead-analysis-alican_inan/
│   ├── team_lead_report_alican_inan_*.xlsx
│   └── summary_alican_inan_*.csv
│
└── team-lead-analysis-alican_inan-FULL/
    ├── full_report_*.xlsx
    ├── developer_health_score.csv
    ├── commit_analysis.csv
    └── commit_classifications.csv
```

**Excel Sheets içeriği:**
- Summary: Özet metrikler
- Commits: Tüm commitler
- MRs Created: Oluşturulan MR'lar
- MRs Approved: Approve edilen MR'lar
- MR Comments: Code review yorumları

**Kullanım:**
- Detaylı drill-down analiz
- Spesifik MR/commit araştırması
- Pivot tables
- Custom analysis

---

### 2. user-metrics/

Tüm projelerdeki (Payment + Service Banking) MR data.

```
user-metrics/
├── user-metrics-alican_inan/
│   ├── metrics_alican_inan_*.xlsx
│   └── merge_requests_alican_inan_*.csv
│
└── user-metrics-gokhan_ibrikci/
    └── [similar structure]
```

**İçerik:**
- All MRs: Tüm merge request'ler
- Summary: Lead time, deployment frequency vb.
- Monthly Breakdown: Aylık metrikler

**Kullanım:**
- Cross-project analysis
- Team geçişi (Payment → Service Banking) analizi
- DORA metrics detayları

---

### 3. service-banking/

Service Banking ekibi genel data (16 Ocak 2025 snapshot).

```
service-banking/
├── gitlab_dora_metrics_*.xlsx
├── gitlab_merge_requests_*.csv
└── gitlab_user_stats_*.csv
```

**İçerik:**
- Tüm ekip DORA metrics
- Ekip-wide MR listesi
- User stats karşılaştırma

**Kullanım:**
- Ekip benchmark
- Historical comparison
- Team-wide analysis

---

### 4. archived-reports/

Eski veya deprecated raporlar (referans için saklandı).

```
archived-reports/
├── CRITICAL-FINDING-Alican-Team-Culture.md
├── gokhan_ibrikci-comprehensive-report-*.md
├── mert_kaim-comprehensive-report-*.md
├── alican_inan-comprehensive-report-*.md
├── gokhan-ibrikci-team-lead-analysis.md
└── GOKHAN-QUICK-REF.md
```

**Not:** Bu raporlar güncel DEĞİL. Ana raporlar için [../results/](../results/) kullanın.

---

## 🎯 Kullanım Örnekleri

### Örnek 1: "Mert'in Kasım ayındaki tüm code review yorumlarını görmek istiyorum"

1. `team-lead-analysis/team-lead-analysis-mert_kaim/` aç
2. `team_lead_report_mert_kaim_*.xlsx` dosyasını Excel'de aç
3. "MR Comments" sheet'ine git
4. "created_at" kolonunu filtrele: "2025-11"
5. Tüm yorumları gör

### Örnek 2: "Alican'ın Payment vs Service Banking MR dağılımı?"

1. `user-metrics/user-metrics-alican_inan/` aç
2. `metrics_alican_inan_*.xlsx` dosyasını aç
3. "All MRs" sheet'inde project_id'ye göre filtrele
4. Aylık breakdown için "Monthly Breakdown" sheet'ine bak

### Örnek 3: "Service Banking ekibi 2025 başında nasıldı?"

1. `service-banking/` klasörüne git
2. `gitlab_user_stats_*.csv` dosyasını aç
3. Tüm ekip üyelerinin lead time, MR count vb. karşılaştır

---

## 📊 Data Freshness

| Klasör | Data Tarihi | Güncellik |
|--------|-------------|-----------|
| team-lead-analysis/ | 20 Ocak 2026 | ✅ Güncel |
| user-metrics/ | 20 Ocak 2026 | ✅ Güncel (Alican için tüm 2025) |
| service-banking/ | 16 Ocak 2025 | ⚠️ Snapshot (2025 ortası) |
| archived-reports/ | Various | ❌ Deprecated |

---

## 🔄 Data Güncelleme

Raporları yeniden oluşturmak için:

```bash
# Team lead analysis
python3 gitlab_team_lead_analysis.py "username"

# User metrics (all projects)
python3 gitlab_user_metrics.py "username"

# Comprehensive report
python3 generate_comprehensive_report.py "username"

# Service banking ekip data
python3 gitlab_dora_metrics.py
```

---

## ⚠️ Notlar

- Excel dosyaları manuel düzenlenmemeli (raw data)
- Analiz için pivot tables kullanın
- Archived raporlar sadece referans için
- Güncel bulgular için ../results/ raporlarını kullanın

---

*Dataset last updated: 2026-01-20*
