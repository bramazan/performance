# Payment Ekibi Dashboard Analiz Planı

**Oluşturulma:** 2026-01-26
**Hedef:** Payment ekibi için kapsamlı performans dashboard'u oluşturma
**Referans:** docs/payment.md

---

## 📋 Ekip Üyeleri ve Kapsam

### 🔧 GitLab + Jira Analizi Yapılacaklar (7 kişi)

| # | İsim | GitLab Username | Rol | Analiz Dönemi | Notlar |
|---|------|----------------|-----|--------------|--------|
| 1 | **Resul Bozdemir** | @resul.bozdemir | Backend Developer | Ağustos-Aralık 2025 | Service Banking'den transfer |
| 2 | **Alican İnan** | @alican.inan | Developer | Ocak-Temmuz 2025 | Ağustos'ta Service Banking'e geçti |
| 3 | **Volkan Kurt** | @volkan.kurt | Software Architect | Tüm 2025 | Kompleks işler lead |
| 4 | **Mustafa Çolakoğlu** | @mustafa.colakoglu | Backend Developer | Tüm 2025 | ❌ Yeni rapor gerekli |
| 5 | **Anıl Sakaryalı** | @anil.sakaryali | Backend Developer | Haziran-Aralık 2025 | Haziran'da başladı |
| 6 | **İzzettin Hallaçoğlu** | @izzettin.hallacoglu | Team Lead | 11 Kas 2024 - 15 Oca 2025 | 2 aylık deneme süresi |
| 7 | **Yasir Arslan** | @yasir.arslan | Stajyer | Aralık 2025 sonu | Yeni katıldı |

### 📊 Sadece Jira Analizi Yapılacaklar (3 kişi)

| # | İsim | Rol | Jira Board | Analiz Dönemi |
|---|------|-----|-----------|--------------|
| 8 | **Metin İsfendiyar** | İş Analisti | TPAY | Tüm 2025 (✅ Mevcut rapor var) |
| 9 | **Tahsin Civelek** | Product Owner | BPAY | Tüm 2025 |
| 10 | **Bilal Cihangir** | Product Owner | BPAY | Tüm 2025 |

### 📦 Mevcut Raporlar (Service Banking verileri - Payment için opsiyonel)

| İsim | Rol | Durum |
|------|-----|-------|
| Ahmet Sağlam | Pos Destek Uzmanı | ✅ Rapor var (results/2025/ahmet-saglam/) |
| Anıl Akkaya | Pos Destek Uzmanı | ✅ Rapor var (results/2025/anil-akkaya/) |
| Mehmet Yetiş | QA Developer | ✅ Rapor var (results/2025/mehmet-yetis/) |
| Yakup Doğan | QA Developer | ✅ Rapor var (results/2025/yakup-dogan/) |

---

## 🎯 Jira Board Yapısı

### TPAY - Tech Board
**URL:** https://odeal.atlassian.net/jira/software/c/projects/TPAY/boards/212
**Amaç:** Sprint koşan yer, ekip verileri
**Kullanım:** Developer ve BA performans metrikleri
**Metrikler:**
- Sprint velocity
- Issue completion rate
- Bug vs Feature ratio
- Cycle time

### BPAY - Business Board
**URL:** https://odeal.atlassian.net/jira/software/c/projects/BPAY/boards/195
**Amaç:** Product Owner + İş birimi takibi
**Kullanım:** Product Owner performans metrikleri (Kritik!)
**Metrikler:**
- Requirement definition rate
- Story approval time
- Backlog refinement efficiency
- Business value delivery

---

## 🔄 İş Akışı

### Faz 1: GitLab Veri Toplama (7 kişi)

**Yeni Script Gerekli:**
```bash
# Mustafa Çolakoğlu için
python scripts/gitlab/gitlab_user_metrics.py --username mustafa.colakoglu --start 2025-01-01 --end 2025-12-31

# Anıl Sakaryalı için
python scripts/gitlab/gitlab_user_metrics.py --username anil.sakaryali --start 2025-06-01 --end 2025-12-31

# İzzettin Hallaçoğlu için
python scripts/gitlab/gitlab_user_metrics.py --username izzettin.hallacoglu --start 2024-11-11 --end 2025-01-15

# Yasir Arslan için
python scripts/gitlab/gitlab_user_metrics.py --username yasir.arslan --start 2025-12-20 --end 2025-12-31
```

**Mevcut Scriptleri Güncelle:**
```bash
# Resul - Payment dönemi için filtrele (Ağustos-Aralık)
python scripts/analyze_resul_gitlab.py --start 2025-08-01 --end 2025-12-31

# Alican - Payment dönemi için filtrele (Ocak-Temmuz)
python scripts/gitlab/gitlab_user_metrics.py --username alican.inan --start 2025-01-01 --end 2025-07-31

# Volkan - Tüm yıl (mevcut rapor kullanılabilir)
# results/2025/volkan-kurt/developer-report-2025.md
```

**Çıktılar:**
```
results/2025/payment/
├── mustafa-colakoglu/
│   └── developer-report-2025.md
├── anil-sakaryali/
│   └── developer-report-2025.md
├── izzettin-hallacoglu/
│   └── developer-report-2025.md
├── yasir-arslan/
│   └── intern-report-2025.md
├── resul-bozdemir/
│   └── developer-report-2025.md
├── alican-inan/
│   └── developer-report-2025.md
└── volkan-kurt/
    └── developer-report-2025.md
```

---

### Faz 2: Jira TPAY Veri Toplama (Tech Board - 8 kişi)

**Target:** Tüm developers + BA (Metin)

**JQL Query Template:**
```jql
project = TPAY
AND created >= "2025-01-01"
AND created <= "2025-12-31"
AND (assignee = "kullanici_email" OR reporter = "kullanici_email")
ORDER BY created DESC
```

**Script Örnekleri:**
```bash
# Mustafa için
python scripts/jira/jira_team_analysis.py --project TPAY --user mustafa.colakoglu@odeal.com.tr

# Anıl Sakaryalı için (Haziran başlangıç)
python scripts/jira/jira_team_analysis.py --project TPAY --user anil.sakaryali@odeal.com.tr --start 2025-06-01

# İzzettin için
python scripts/jira/jira_team_analysis.py --project TPAY --user izzettin.hallacoglu@odeal.com.tr --start 2024-11-11 --end 2025-01-15

# Yasir için
python scripts/jira/jira_team_analysis.py --project TPAY --user yasir.arslan@odeal.com.tr --start 2025-12-20

# Metin için (mevcut script var - güncelle)
python scripts/jira/jira_metin_isfendiyar_analysis.py --project TPAY
```

---

### Faz 3: Jira BPAY Veri Toplama (Business Board - 2 Product Owner)

**Target:** Tahsin Civelek, Bilal Cihangir

**JQL Query Template:**
```jql
project = BPAY
AND created >= "2025-01-01"
AND created <= "2025-12-31"
AND (reporter = "product_owner_email" OR assignee = "product_owner_email")
ORDER BY created DESC
```

**Script (Yeni):**
```bash
# Tahsin Civelek için
python scripts/jira/jira_po_analysis.py --project BPAY --user tahsin.civelek@odeal.com.tr --role "Product Owner"

# Bilal Cihangir için
python scripts/jira/jira_po_analysis.py --project BPAY --user bilal.cihangir@odeal.com.tr --role "Product Owner"
```

**Metrikler (PO-specific):**
- Created issues count
- Story point estimation accuracy
- Refinement meeting efficiency
- Stakeholder communication (issue descriptions quality)
- Backlog health (age of issues)

**Çıktılar:**
```
results/2025/payment/
├── tahsin-civelek/
│   └── po-report-2025.md
├── bilal-cihangir/
│   └── po-report-2025.md
└── metin-isfendiyar/
    └── ba-report-2025.md
```

---

### Faz 4: Markdown Rapor Derleme

**Format (Developer):**
```markdown
# [İsim] (Payment Team) - GitLab Developer Report

**Analysis Period:** [Tarih Aralığı]
**Team:** Payment
**GitLab Username:** @username

## 📊 Executive Summary
- Total Merge Requests: X
- Average Lead Time: Y hours
- Performance Grade: [ELITE/VERY GOOD/GOOD/NEEDS IMPROVEMENT]

## 1. 📈 Key Performance Indicators (DORA Metrics)
## 2. 🎯 Work Distribution & Contribution Breakdown
## 3. ⏰ Temporal Analysis
## 4. 🔄 Code Review Activity
## 5. 💡 Recommendations
```

**Format (Product Owner):**
```markdown
# [İsim] (Payment Team) - Product Owner Report

**Analysis Period:** 2025-01-01 to 2025-12-31
**Team:** Payment
**Board:** BPAY (Business Board)

## 📊 Executive Summary
- Total Issues Created: X
- Story Points Delivered: Y
- Refinement Efficiency: Z%

## 1. 📋 Backlog Management
## 2. 🎯 Business Value Delivery
## 3. 📊 Stakeholder Communication
## 4. 🔄 Sprint Planning Effectiveness
## 5. 💡 Recommendations
```

---

### Faz 5: Dashboard HTML Derleme

**File:** `dashboard/index_payment.html`

**Data Sources:**
```
Tüm markdown raporlardan (10+ kişi):
→ Executive summaries
→ Key metrics
→ Health scores
→ Team composition
```

**Dashboard Sections:**
1. **Header:** "Payment Ekibi Paneli"
2. **Overview:**
   - Ekip kapasitesi (10 kişi teknik ekip)
   - Teslim performansı (TPAY sprint metrikleri)
   - Kod kalitesi (Bug ratio)
   - Süreç uyumu (MR usage)

3. **Talent Section:**
   - 10 kişi kartları (Developer + PO + BA)
   - Health scores
   - DORA metrikleri

4. **Health Section:**
   - Ekip sağlığı KPI'ları
   - İşbirliği kültürü
   - Rol dağılımı

5. **Tech Section:**
   - Teknik borç
   - Pipeline durumu

6. **Projects Section:**
   - 2025 özeti
   - 2026 roadmap (Kredi, Asıl Kart, Açık Bankacılık)

7. **Ecosystem Section:**
   - Sponsorlar (CTO, Eng Manager, Product Head)
   - İş paydaşları

---

## 📝 Checklist

### GitLab Raporlar
- [ ] Mustafa Çolakoğlu - Yeni rapor
- [ ] Anıl Sakaryalı - Yeni rapor
- [ ] İzzettin Hallaçoğlu - Yeni rapor
- [ ] Yasir Arslan - Yeni rapor
- [ ] Resul Bozdemir - Payment dönemi güncelle
- [ ] Alican İnan - Payment dönemi güncelle
- [ ] Volkan Kurt - Mevcut rapor doğrula

### Jira TPAY Raporlar
- [ ] Mustafa Çolakoğlu
- [ ] Anıl Sakaryalı
- [ ] İzzettin Hallaçoğlu
- [ ] Yasir Arslan
- [ ] Resul Bozdemir
- [ ] Alican İnan
- [ ] Volkan Kurt
- [ ] Metin İsfendiyar - Güncelle

### Jira BPAY Raporlar
- [ ] Tahsin Civelek - Yeni PO raporu
- [ ] Bilal Cihangir - Yeni PO raporu

### Dashboard
- [ ] index_payment.html güncelle
- [ ] Tüm kişi kartlarını ekle
- [ ] Ekip metriklerini hesapla
- [ ] Projeleri güncelle (Ödeal Kart, Portal, Kredi, vb)

---

## 🚀 Öncelikler

1. **Yüksek:** Yeni raporlar (Mustafa, Anıl S., İzzettin, Yasir) - 4 kişi
2. **Orta:** Mevcut rapor güncellemeleri (Resul, Alican Payment filtreleme)
3. **Orta:** PO raporları (Tahsin, Bilal - yeni script gerekli)
4. **Düşük:** Dashboard HTML montajı (tüm data toplandıktan sonra)

---

## 📌 Notlar

- **İzzettin:** Sadece 2 ay çalıştı, "needs improvement" flagı koyma
- **Yasir:** Stajyer, kısa süre, "onboarding phase" olarak işaretle
- **Resul & Alican:** Service Banking raporları var, Payment için filtrele
- **BPAY Board:** Product Owner performansı için kritik, özel metrikler gerekli
- **TPAY Board:** Asıl sprint verileri burada

---

**Son Güncelleme:** 2026-01-26
**Hazırlayan:** Performance Analysis System
**Durum:** 📋 Planning Phase
