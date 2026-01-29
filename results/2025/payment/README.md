# Payment Ekibi - 2025 Performans Raporları

**Ekip:** Payment Team
**Analiz Dönemi:** 2025 (Kişiye özel tarih aralıkları var)
**Jira Boards:**
- TPAY (Tech Board): https://odeal.atlassian.net/jira/software/c/projects/TPAY/boards/212
- BPAY (Business Board): https://odeal.atlassian.net/jira/software/c/projects/BPAY/boards/195

---

## 📁 Klasör Yapısı

```
payment/
├── README.md                      # Bu dosya
├── resul-bozdemir/               # Backend Developer (Ağustos-Aralık)
├── alican-inan/                  # Developer (Ocak-Temmuz)
├── volkan-kurt/                  # Software Architect
├── mustafa-colakoglu/            # Backend Developer
├── anil-sakaryali/               # Backend Developer (Haziran'dan itibaren)
├── izzettin-hallacoglu/          # Team Lead (11 Kasım - 15 Ocak)
├── yasir-arslan/                 # Stajyer (Aralık sonu)
├── metin-isfendiyar/             # İş Analisti
├── tahsin-civelek/               # Product Owner
└── bilal-cihangir/               # Product Owner
```

---

## 👥 Ekip Üyeleri

### Backend Developers (7 kişi)

| İsim | GitLab | Durum | Analiz Dönemi |
|------|--------|-------|--------------|
| **Resul Bozdemir** | @resul.bozdemir | Service Banking'den transfer | Ağustos-Aralık 2025 |
| **Alican İnan** | @alican.inan | Service Banking'e transfer | Ocak-Temmuz 2025 |
| **Volkan Kurt** | @volkan.kurt | Software Architect | Tüm 2025 |
| **Mustafa Çolakoğlu** | @mustafa.colakoglu | Backend Developer | Tüm 2025 |
| **Anıl Sakaryalı** | @anil.sakaryali | Backend Developer | Haziran-Aralık 2025 |
| **İzzettin Hallaçoğlu** | @izzettin.hallacoglu | Team Lead (2 aylık deneme) | 11 Kasım 2024 - 15 Ocak 2025 |
| **Yasir Arslan** | @yasir.arslan | Stajyer | Aralık 2025 sonu |

### Business & Product (3 kişi)

| İsim | Rol | Jira Board |
|------|-----|-----------|
| **Metin İsfendiyar** | İş Analisti | TPAY (Tech) |
| **Tahsin Civelek** | Product Owner | BPAY (Business) |
| **Bilal Cihangir** | Product Owner | BPAY (Business) |

---

## 📊 Rapor Formatları

### Developer Report
```
developer-report-2025.md
├── Executive Summary
├── Key Performance Indicators (DORA Metrics)
├── Work Distribution & Contribution Breakdown
├── Temporal Analysis
├── Code Review Activity
└── Recommendations
```

### Product Owner Report
```
po-report-2025.md
├── Executive Summary
├── Backlog Management
├── Business Value Delivery
├── Stakeholder Communication
├── Sprint Planning Effectiveness
└── Recommendations
```

### Business Analyst Report
```
ba-report-2025.md
├── Executive Summary
├── Requirement Analysis
├── Story Creation & Refinement
├── Sprint Collaboration
├── Documentation Quality
└── Recommendations
```

---

## 🎯 Metrikler

### GitLab (Developer)
- Merge Requests (count, rate, approval rate)
- Lead Time (average, median, distribution)
- Code Review Activity (given vs received)
- Commit Patterns (frequency, size, timing)
- DORA Metrics (deployment frequency, change failure rate)

### Jira TPAY (Tech Board)
- Issues (created, assigned, resolved)
- Sprint Performance (velocity, completion rate)
- Bug vs Feature ratio
- Cycle Time (average time to resolution)
- Story Points (delivered, estimated accuracy)

### Jira BPAY (Business Board)
- Requirements Created (count, quality)
- Refinement Efficiency (story readiness)
- Stakeholder Communication (description quality score)
- Backlog Health (age distribution)
- Business Value Delivery (story point value)

---

## 🚀 Kullanım

### Rapor Oluşturma

```bash
# GitLab raporları
python scripts/gitlab/gitlab_user_metrics.py --username <gitlab_username> --output results/2025/payment/<name>/

# Jira TPAY raporları (developers)
python scripts/jira/jira_team_analysis.py --project TPAY --user <email> --output results/2025/payment/<name>/

# Jira BPAY raporları (product owners)
python scripts/jira/jira_po_analysis.py --project BPAY --user <email> --output results/2025/payment/<name>/
```

### Dashboard Oluşturma

```bash
# Tüm raporları derleyerek dashboard oluştur
python scripts/generate_payment_dashboard.py --input results/2025/payment/ --output dashboard/index_payment.html
```

---

## 📌 Notlar

- **Resul & Alican:** Her ikisi de kısmi dönem (transfer durumu)
- **İzzettin:** 2 aylık deneme süresi, kısa dönem analizi
- **Yasir:** Stajyer, onboarding phase olarak değerlendir
- **BPAY Board:** Product Owner performansı için kritik metrikler içerir
- **TPAY Board:** Sprint koşan yer, ekip verimlilik verileri

---

**Oluşturulma:** 2026-01-26
**Son Güncelleme:** 2026-01-26
**Referans:** docs/payment.md, docs/tasks/payment-dashboard-analysis.md
