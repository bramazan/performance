# Performance Analysis Scripts

Bu klasör, Odeal performans değerlendirmeleri için kullanılan Python scriptlerini içerir.

---

## 📁 Klasör Yapısı

```
scripts/
├── README.md              # Bu dosya
├── gitlab/                # GitLab ile ilgili scriptler
├── jira/                  # Jira ile ilgili scriptler
├── analyze_*.py           # Analiz scriptleri
└── generate_*.py          # Rapor üretme scriptleri
```

---

## 🔧 GitLab Scripts

**Klasör:** [gitlab/](gitlab/)

- `gitlab_dora_metrics.py` - DORA metrikleri toplama
- `gitlab_user_metrics.py` - Kullanıcı bazlı metrikler
- `gitlab_team_lead_analysis.py` - Team lead analizi
- `gitlab_enhanced_metrics.py` - Gelişmiş metrikler
- `gitlab_commits_metrics.py` - Commit analizi
- `gitlab_discover.py` - GitLab kaynak keşfi

---

## 📊 Jira Scripts

**Klasör:** [jira/](jira/)

- `jira_team_analysis.py` - Team analizi
- `jira_team_analysis_rest.py` - REST API ile team analizi
- `jira_simple_analysis.py` - Basit analiz
- `jira_metin_isfendiyar_analysis.py` - Bireysel analiz (Metin)
- `jira_metin_combined_analysis.py` - Kombine analiz (Metin)
- `jira_metin_tpay_analysis.py` - TPay analizi (Metin)
- `jira_resul_bozdemir_analysis.py` - Bireysel analiz (Resul)
- `jira_debug.py` - Debug aracı
- `jira_list_users.py` - Kullanıcı listesi

---

## 🔍 Analiz Scripts

**Klasör:** Ana dizin

- `analyze_bug_ratio.py` - Bug oranı analizi
- `analyze_resul_bozdemir.py` - Bireysel analiz (Resul)
- `analyze_resul_gitlab.py` - GitLab analizi (Resul)
- `analyze_resul_simple.py` - Basit analiz (Resul)

---

## 📝 Rapor Üretme Scripts

**Klasör:** Ana dizin

- `generate_comprehensive_report.py` - Kapsamlı rapor üretimi
- `generate_metin_summary.py` - Özet rapor (Metin)

---

## 🚀 Kullanım

### Gereksinimler

```bash
pip install -r ../requirements.txt
```

### Environment Variables

`.env` dosyası oluşturun:

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

### GitLab Metrikleri

```bash
cd gitlab/
python gitlab_dora_metrics.py
```

### Jira Analizi

```bash
cd jira/
python jira_team_analysis.py
```

### Rapor Üretimi

```bash
python generate_comprehensive_report.py
```

---

## 📖 Detaylı Dökümantasyon

- GitLab araçları için: [../README.md](../README.md)
- DORA metrikleri: [../docs/enhanced-metrics-guide.md](../docs/enhanced-metrics-guide.md)

---

*Son güncelleme: 2026-01-22*
