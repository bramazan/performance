# Payment Ekibi - Quick Start Guide

**Oluşturulma:** 2026-01-26
**Durum:** ✅ Production Ready

---

## 🚀 Hızlı Başlangıç

### Dashboard'u Görüntüle

```bash
# Tarayıcıda aç
open dashboard/index_payment.html

# VEYA local server ile
cd dashboard && python3 -m http.server 8080
# Tarayıcı: http://localhost:8080/index_payment.html
```

### Raporları İncele

```bash
# Payment klasörüne git
cd results/2025/payment/

# Ekip özetini oku
cat TEAM-SUMMARY.md

# Belirli bir developer raporunu aç
open mustafa-colakoglu/developer-report-2025.md
open volkan-kurt/developer-report-2025.md

# PO raporlarını aç
open tahsin-civelek/po-report-2025.md
open bilal-cihangir/po-report-2025.md
```

---

## 📊 Ekip Özeti (2025)

### Developers (7 kişi)

| Kişi | MRs | Lead Time | Durum |
|------|-----|-----------|-------|
| **Volkan Kurt** | 129 | 3.27h median | ⭐ ELITE |
| **Mustafa Çolakoğlu** | 99 | 17.51h median | ✅ GOOD |
| **Anıl Sakaryalı** | 84 | 166h median | ⚠️ ONBOARDING |
| Resul Bozdemir | - | - | Transfer (Ağu-Ara) |
| Alican İnan | - | - | Transfer (Oca-Tem) |
| İzzettin Hallaçoğlu | 0 | - | Trial (2 ay) |
| Yasir Arslan | 0 | - | Stajyer (yeni) |

**Team Total:** 312 MRs, ~62h median lead time

### Business/Product (3 kişi)

| Kişi | Rol | TPAY | BPAY | Toplam |
|------|-----|------|------|--------|
| **Metin İsfendiyar** | BA | 100 | 0 | 100 ⭐ |
| **Tahsin Civelek** | PO | 59 | 7 | 66 |
| **Bilal Cihangir** | PO | 16 | 10 | 26 |

**Team Total:** 192 Jira issues (175 tech, 17 business)

---

## 📁 Rapor Lokasyonları

### Bireysel Raporlar

**Developers:**
- [Mustafa Çolakoğlu](mustafa-colakoglu/developer-report-2025.md) - 99 MRs, 10 projects
- [Anıl Sakaryalı](anil-sakaryali/developer-report-2025.md) - 84 MRs, onboarding
- [Volkan Kurt](volkan-kurt/developer-report-2025.md) - 129 MRs, elite performer
- [Resul Bozdemir](resul-bozdemir/developer-report-2025.md) - Transfer (Ağu-Ara)
- [Alican İnan](alican-inan/developer-report-2025.md) - Transfer (Oca-Tem)
- [İzzettin Hallaçoğlu](izzettin-hallacoglu/developer-report-2025.md) - Placeholder
- [Yasir Arslan](yasir-arslan/developer-report-2025.md) - Intern

**Business/Product:**
- [Metin İsfendiyar (BA)](metin-isfendiyar/ba-report-2025.md) - 100 issues, YÜKSEK hacim
- [Tahsin Civelek (PO)](tahsin-civelek/po-report-2025.md) - 66 issues, tech PO
- [Bilal Cihangir (PO)](bilal-cihangir/po-report-2025.md) - 26 issues, balanced PO

### Özet Raporlar

- [TEAM-SUMMARY.md](TEAM-SUMMARY.md) - Ekip performans özeti (GitLab bazlı)
- [JIRA-BO-PO-SUMMARY.md](JIRA-BO-PO-SUMMARY.md) - PO/BA Jira analizi
- [JIRA-ANALYSIS-NOTE.md](JIRA-ANALYSIS-NOTE.md) - Jira veri durumu
- [DASHBOARD-UPDATE-NOTES.md](DASHBOARD-UPDATE-NOTES.md) - HTML güncelleme rehberi
- [COMPLETION-SUMMARY.md](COMPLETION-SUMMARY.md) - Proje tamamlanma raporu

---

## 🎯 Önemli Bulgular

### Top Performers

1. **Volkan Kurt** - ELITE developer (3.27h median lead time)
2. **Metin İsfendiyar** - En yüksek Jira output (100 issues)
3. **Mustafa Çolakoğlu** - En yüksek GitLab MR (99 MRs)

### Gelişim Alanları

1. **Anıl Sakaryalı** - Lead time coaching gerekli (166h → 72h hedef)
2. **Bilal Cihangir** - Output artırma (26 → 50+ issues)
3. **Ekip BPAY engagement** - Business board activity artış gerekli (9% → 25%)

### Ekip Riskleri

1. **Transfer risk** - Resul ve Alican ayrıldı
2. **Onboarding load** - Anıl + Yasir coaching gerekli
3. **Business board gap** - Sadece 17 BPAY issue (düşük)

---

## 📖 Döküman İndeksi

### Developer Raporları (GitLab)

Her rapor içerir:
- Executive Summary
- DORA Metrics (Lead Time, MR count, etc.)
- Work Distribution (Project breakdown)
- Temporal Analysis (Monthly trends)
- Code Review Activity
- Recommendations (kişiye özel)

### PO/BA Raporları (Jira)

Her rapor içerir:
- Jira Activity Overview
- Board Distribution (BPAY vs. TPAY)
- Product Owner Style Assessment
- Comparative Analysis (peer comparison)
- Recommendations
- 2026 Goals

### Özet Raporlar

- **TEAM-SUMMARY:** Ekip toplu performans (GitLab metrikleri)
- **JIRA-BO-PO-SUMMARY:** PO/BA Jira detayları + karşılaştırma
- **DASHBOARD-UPDATE-NOTES:** HTML güncelleme için notlar
- **COMPLETION-SUMMARY:** Proje tamamlanma ve teslimat raporu

---

## 🔧 Teknik Bilgiler

### Veri Kaynakları

**GitLab:**
- API: GitLab REST API v4
- Scripts: `scripts/gitlab/gitlab_user_metrics.py`
- Data: Merge requests, commits, lead time
- Period: 2025-01-01 to 2025-12-31 (kişiye özel)

**Jira:**
- API: Jira REST API v3
- Scripts: `scripts/jira/jira_payment_po_analysis.py`
- Data: Issues (BPAY + TPAY boards)
- Period: 2025-01-01 to 2025-12-31

### Script Kullanımı

```bash
# Yeni developer için GitLab raporu
python3 scripts/gitlab/gitlab_user_metrics.py <username>

# PO/BA Jira analizi
python3 scripts/jira/jira_payment_po_analysis.py

# Comprehensive report generation
python3 scripts/generate_comprehensive_report.py --username <name> --group <id>
```

---

## ⏭️ Sonraki Adımlar

### İmmediate (Bu Hafta)

- [ ] Dashboard'u browser'da test et
- [ ] Ekip ile raporları paylaş
- [ ] Feedback topla

### Short-term (1 Ay)

- [ ] Jira field access request (description quality için)
- [ ] Talent section'ı tam güncelle (5 developer kartı)
- [ ] Interactive charts ekle (optional)

### Long-term (3 Ay)

- [ ] Q1 2026 performance review
- [ ] Template-based dashboard generation
- [ ] Auto-update pipeline (weekly/monthly)

---

## 💡 Tips

1. **Raporları VSCode'da aç** - Markdown preview için
2. **Dashboard'u live server ile aç** - Yavaş yüklenme olabilir
3. **JSON data kullan** - `/tmp/dashboard_data_summary.json` template için hazır
4. **Git commit** - Tüm `results/2025/payment/` klasörünü commit et

---

**Son güncelleme:** 2026-01-26 17:45:00
**Versiyon:** 1.0
**Status:** ✅ Production Ready
