# Payment Ekibi - Jira Analiz Notu

**Tarih:** 2026-01-26
**Projeler:** TPAY (Tech Board), BPAY (Business Board)

---

## 📋 Jira Project Members (TPAY)

Payment ekibi üyeleri TPAY projesinde kayıtlı:

| İsim | Account ID | Rol |
|------|-----------|-----|
| **Mustafa Çolakoğlu** | 63be559698bf50328c689f0f | Developer |
| **Anıl Sakaryalı** | 712020:10781cc8-0c44-4906-87b5-e5f03d7da6fc | Developer |
| **İzzettin Hallaçoğlu** | 712020:c706f86c-bdbf-41b6-a0b9-1b0e452ef7c3 | Team Lead (trial) |
| **Yasir Arslan** | 712020:158b24c9-0b8f-4c93-ba26-597eb5c7280c | Intern |
| **Metin İsfendiyar** | 712020:cfd51bc9-798b-4bdf-a360-681849c4215e | Business Analyst |
| **Tahsin Civelek** | 712020:5539afbb-7f6e-4492-b448-b4e3f9e3ffbb | Product Owner |
| **Bilal Cihangir** | 5e9421738beda00c1f29f571 | Product Owner |

**Not:** Resul Bozdemir, Alican İnan, Volkan Kurt TPAY member listesinde görünmüyor (eski TSB projesi kullanıyor olabilirler veya TPAY'e sonradan eklenmemiş olabilir).

---

## 🔍 Veri Toplama Durumu

### TPAY Board Analysis (Tech Board)

**URL:** https://odeal.atlassian.net/jira/software/c/projects/TPAY/boards/212

**Durum:** ⚠️ **Sınırlı Veri**
- Son 100 issue sorgulaması yapıldı (2025 yılı için)
- **Reporter/Assignee listesi boş** - Bu şu anlama gelebilir:
  1. TPAY projesi yeni oluşturulmuş, henüz issue oluşturulmamış
  2. Ekip farklı bir Jira project kullanıyor (örn: TSB - Service Banking)
  3. 2025 yılında TPAY'de aktivite olmamış

**Alternatif Yaklaşım:**
Payment ekibi için Jira verileri TSB (Service Banking) projesinden çekilebilir, çünkü:
- Resul Bozdemir'in mevcut Jira raporu TSB bazlı (`jira_resul_bozdemir_analysis.py`)
- Alican İnan Service Banking ekibine transfer oldu (Ağustos 2025)
- Volkan Kurt Finance Team olarak gösterilse de TPAY projelerinde çalışıyor

---

### BPAY Board Analysis (Business Board)

**URL:** https://odeal.atlassian.net/jira/software/c/projects/BPAY/boards/195

**Durum:** ✅ **Product Owners Kayıtlı**
- Tahsin Civelek: Kayıtlı (accountId: 712020:5539afbb-7f6e-4492-b448-b4e3f9e3ffbb)
- Bilal Cihangir: Kayıtlı (accountId: 5e9421738beda00c1f29f571)

**Action Required:**
BPAY projesi için özel Product Owner analiz scripti oluşturulmalı:
- Created issues count
- Story acceptance rate
- Backlog refinement activity
- Stakeholder communication quality

---

## 💡 Öneriler

### Kısa Dönem (Dashboard için)

Payment ekibi dashboard'u için Jira analizini şu şekilde yapabiliriz:

**Opsiyon 1: TSB Projesinden Çek (Recommended)**
- Resul, Alican, Volkan için mevcut TSB verileri var
- Mustafa, Anıl için TSB projesinde arama yap
- Payment ekibi members genellikle her iki projede de (TSB + TPAY) çalışıyor

**Opsiyon 2: TPAY + TSB Combined**
- TPAY'deki minimal veriyi TSB verileriyle birleştir
- Multi-project analysis (hem TSB hem TPAY)

**Opsiyon 3: Sadece GitLab Verisi ile Dashboard**
- Jira analizini atlayıp sadece GitLab verisiyle dashboard oluştur
- Jira raporlarını ileriki aşamada ekle

### Uzun Dönem

1. **TPAY Projesini Aktif Kullanım:** Ekibin TPAY'e geçiş yapmasını sağla
2. **Jira Workflow İyileştirme:** Tüm developers için TPAY projesi zorunlu
3. **Product Owner Tracking:** BPAY için özel metrikler oluştur

---

## 📊 Mevcut Veri Durumu (Payment Ekibi)

| Kişi | GitLab Raporu | Jira TPAY | Jira TSB | Toplam Veri |
|------|--------------|-----------|----------|-------------|
| **Mustafa Çolakoğlu** | ✅ 99 MRs | ❓ Unknown | ❓ Unknown | GitLab only |
| **Anıl Sakaryalı** | ✅ 84 MRs | ❓ Unknown | ❓ Unknown | GitLab only |
| **Resul Bozdemir** | ✅ Mevcut | ❌ None | ✅ Mevcut | GitLab + Jira (TSB) |
| **Alican İnan** | ✅ Mevcut | ❌ None | ✅ Likely | GitLab + Jira (TSB) |
| **Volkan Kurt** | ✅ 129 MRs | ❌ None | ❓ Unknown | GitLab only |
| **İzzettin Hallaçoğlu** | ❌ 0 MRs | ❌ None | ❓ Unknown | No data |
| **Yasir Arslan** | ❌ 0 MRs | ❌ None | ❌ None | No data (intern) |
| **Metin İsfendiyar (BA)** | N/A | ✅ Mevcut | ✅ Mevcut | Jira (TPAY+TSB) |
| **Tahsin Civelek (PO)** | N/A | ❓ Unknown | ❓ Unknown | BPAY needed |
| **Bilal Cihangir (PO)** | N/A | ❓ Unknown | ❓ Unknown | BPAY needed |

---

## 🎯 Dashboard İçin Karar

**Önerilen:** Dashboard'u şu anki GitLab verileriyle oluştur:

1. **7 Developer için GitLab metrikleri mevcut** (Mustafa, Anıl, Resul, Alican, Volkan + 2 placeholder)
2. **Metin için mevcut Jira raporu var** (BA perspective)
3. **Product Owners için:** Basit not ekle ("BPAY board, detaylı analiz yapılacak")

**Dashboard Sections:**
- **Talent:** 7 developer kartları (GitLab bazlı DORA metrics)
- **Business Analyst:** Metin'in cartı (mevcut Jira raporundan)
- **Product:** Tahsin & Bilal için genel bilgi kartları

---

## 📝 Sonraki Adımlar

1. ✅ GitLab raporları tamamlandı (8 kişi)
2. ⏳ Dashboard HTML oluştur (GitLab verisiyle)
3. 🔄 Jira TPAY/BPAY detaylı analiz (Phase 2, opsiyonel)

---

**Generated:** 2026-01-26 16:15:00
**Analyzer:** Payment Team Performance System
**Status:** GitLab Complete, Jira Pending Detailed Analysis
