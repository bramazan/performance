# Service Banking Team - Projects in 2025

**Period:** 2025-01-01 to 2025-12-31
**Data Source:** Jira TSB Board (1,000 issues analyzed)
**Generated:** 2026-01-20

---

## 📊 Project Overview

Ekip 2025 yılında **13 farklı servis/proje** üzerinde çalıştı. Toplamda **1,000 Jira issue** oluşturuldu.

---

## 🏗️ Main Projects (Issue Count)

### 1. Card Manager - **301 issues (30.1%)** ⭐⭐⭐

**Primary Project** - Ekibin ana odak alanı

**Kart yönetim servisi:**
- Kart oluşturma/güncelleme/sorgulama
- Card işlemleri API'leri
- Mail order / e-commerce card operations
- Transaction management

**Örnek Issues:**
- `TSB-50`: Kartı MailOrder'a Kapalı Olan Kullanıcıların Portal'den Online'a Açabilmesi
- `TSB-45`: Kart Bilgilerinin Güncellenmesi
- `TSB-39`: Card İşlemleri İçin API ve Veri Tabanı Mimari Tasarımı

**Focus:** %30 of team's effort - Largest project

---

### 2. Fiba Integration - **64 issues (6.4%)** ⭐

**Banking Integration** - Fibabanka entegrasyonu

**Fiba Gateway ve banka bağlantıları:**
- FibaGateway servisi
- Banking API integration
- Gateway katmanı mimari
- Card operations with Fiba

**Örnek Issues:**
- `TSB-40`: Gateway Katmanı Mimari Tasarımı ve Fibabanka Kurallarının Çıkarılması
- `TSB-108`: CardManager projesinin FibaGateway projesi ile bağlantısının sağlanması
- `TSB-83`: FibaGateway Projesinin reposunun oluşturulması

**Focus:** Integration layer work

---

### 3. Portal Manager - **42 issues (4.2%)** ⭐

**Web Portal Backend** - Customer-facing portal

**Portal backend servisi:**
- Backend API'ler
- User interface bağlantıları
- Admin operations
- Instana integration

**Örnek Issues:**
- `TSB-50`: Portal'den kart açma işlemleri
- `TSB-60`: Portal Backend Projesi Instana Entegrasyonu
- `TSB-319`: Yeni ürün yapısı teknik analiz ve portal BFF

**Focus:** Customer portal development

---

### 4. Credit Manager - **33 issues (3.3%)** ✅

**Kredi Yönetim Servisi:**
- Kredi başvuru süreçleri
- Credit listing/querying
- Findex integration
- Admin credit operations

**Örnek Issues:**
- `TSB-502`: Kullanılan kredilerin getCreditList şeklinde çekilebilmesi (admin)
- `TSB-1028`: Test otomasyon - Kredi başvuru testi
- `TSB-908`: Findex kredi sorgusu eklenmeli

**Focus:** Credit management features

---

### 5. Gateway - **26 issues (2.6%)** ✅

**API Gateway Servisi:**
- Odeal Gateway
- Routing ve orchestration
- Card transaction endpoints
- Cross-service communication

**Örnek Issues:**
- `TSB-40`: Gateway Katmanı Mimari Tasarımı
- `TSB-1342`: CardTransactionList ve CardTransactionListExcel endpointleri
- `TSB-108`: CardManager-FibaGateway bağlantısı

**Focus:** Service orchestration

---

### 6. Member Service - **11 issues (1.1%)** ✅

**Üye/Member Yönetimi:**
- Member operations
- User management
- Membership features

**Focus:** User/member management

---

### 7. OTP Service - **7 issues (0.7%)**

**OTP/Authentication:**
- One-time password servisi
- Authentication flows

**Focus:** Security & authentication

---

### 8. Payment - **6 issues (0.6%)**

**Payment İşlemleri:**
- Payment processing
- Transaction management

**Focus:** Payment operations

---

### 9-13. Other Services (< 0.5% each)

- **Credential Service** - 3 issues
- **Scheduler** - 3 issues
- **Retail** - 3 issues
- **Identity Service** - 1 issue
- **Bank Integration** - 1 issue

---

## 📊 Project Distribution Analysis

### By Volume

```
Card Manager        ████████████████████████████████ 301 (30.1%)
Fiba Integration    ███████ 64 (6.4%)
Portal Manager      █████ 42 (4.2%)
Credit Manager      ████ 33 (3.3%)
Gateway             ███ 26 (2.6%)
Others              ██████ 34 (3.4%)
Not Categorized     ████████████████████████████████████████ 500 (50.0%)
```

**Note:** ~50% of issues don't explicitly mention service names (general tasks, testing, operations)

---

## 🎯 Project Focus Areas

### Core Banking Services (414 issues = 41.4%)

**Card Operations Focus:**
- Card Manager: 301 issues ⭐⭐⭐ **Primary**
- Fiba Integration: 64 issues (card-related banking)
- Gateway: 26 issues (card transaction routing)

**Total Card-Related:** ~391 issues (39.1%) of identified work

**Credit Operations:**
- Credit Manager: 33 issues
- Findex integration work

### Supporting Services (20 issues = 2.0%)

- Member: 11 issues
- OTP: 7 issues
- Others: ~8 issues

### Infrastructure & Quality (570 issues = 57%)

**Not service-specific issues:**
- Testing & QA: 313 issues (31.3%)
- General tasks: ~200 issues
- Architecture/design: Multiple
- Operations & meetings: 40 issues

**Interpretation:** Team spends significant time on quality assurance and cross-cutting concerns.

---

## 🔍 Work Pattern Insights

### Primary Focus: Card Banking

**%39 of identifiable work** related to card operations:
- Card Manager service development
- Fiba banking integration
- Card transaction processing
- Gateway routing for cards

**Assessment:** ⭐ **Clear specialization** - Team is card-focused banking team

### Secondary: Credit & Supporting Services

**%7 of work** on credit and support services:
- Credit management
- Member operations
- Authentication (OTP)

**Assessment:** ✅ Diversified but secondary focus

### Quality-First Approach

**%31.3 of ALL work** is testing/QA:
- Cross checks
- Test issues
- Quality validation

**Combined with %1.8 bug ratio** = Excellent quality culture

---

## 📈 Project Evolution (2025)

### H1 (Jan-Jun): Foundation

**Main Activities:**
- Architecture design (Gateway, Fiba)
- Initial Card Manager development
- Portal backend integration

**Volume:** 259 issues (lower)

### H2 (Jul-Dec): Acceleration

**Main Activities:**
- Card Manager heavy development (likely majority of 301 issues)
- Fiba integration ramp-up
- Production features

**Volume:** 741 issues (high)

**Peak (August):** 256 issues
- Likely: Major card feature push
- Alican joined = extra capacity
- Sprint acceleration

---

## 🆚 GitLab-Jira Project Alignment

### GitLab Repositories (from earlier analysis):

1. card-manager
2. card-manager-v2
3. fiba-integration / bank-integration
4. portal-manager
5. credit-manager
6. odeal-gateway
7. credential-service
8. otp
9. member
10. service-banking-scheduler
11. identity

**Alignment:** ⭐ **EXCELLENT** - Jira projects match GitLab repos almost 1:1

### Cross-Reference

| Jira Mentions | GitLab Repo | Match |
|---------------|-------------|-------|
| Card Manager (301) | card-manager, card-manager-v2 | ✅ Perfect |
| Fiba Integration (64) | fiba-integration, bank-integration | ✅ Perfect |
| Portal Manager (42) | portal-manager | ✅ Perfect |
| Credit Manager (33) | credit-manager | ✅ Perfect |
| Gateway (26) | odeal-gateway | ✅ Perfect |
| Member (11) | member | ✅ Perfect |
| OTP (7) | otp | ✅ Perfect |
| Credential (3) | credential-service | ✅ Perfect |

**Conclusion:** Good traceability between Jira issues and GitLab repos.

---

## 💡 Key Findings

### 1. Card Banking Specialization ⭐

**39% of work** in card-related services:
- Clear team specialization
- Deep expertise area
- Main value delivery

### 2. Microservices Architecture ✅

**11+ independent services:**
- Well-architected system
- Clear separation of concerns
- Each service has dedicated repo

### 3. Quality-First Culture ⭐⭐⭐

**31.3% QA work + 1.8% bugs:**
- Testing is priority
- Prevents issues before production
- Mature development process

### 4. Tracking Discipline Varies ⚠️

**Some issues generic:**
- ~50% don't mention specific service
- "Test", "Cross Check" issues
- Can make project tracking harder

---

## 📋 Complete Service List (2025)

### Active Development Services (11)

1. **Card Manager** ⭐⭐⭐ (Primary - 301 issues)
2. **Fiba Integration** ⭐ (Banking - 64 issues)
3. **Portal Manager** ⭐ (Customer Portal - 42 issues)
4. **Credit Manager** ✅ (Credit Operations - 33 issues)
5. **Gateway** ✅ (API Gateway - 26 issues)
6. **Member Service** ✅ (User Management - 11 issues)
7. **OTP Service** ✅ (Authentication - 7 issues)
8. **Payment** (Payment Processing - 6 issues)
9. **Credential Service** (Auth - 3 issues)
10. **Scheduler** (Job Scheduling - 3 issues)
11. **Retail** (Retail Operations - 3 issues)

### Emerging Services (New/Minimal)

12. **Identity Service** (SSO/Identity - 1 issue)
13. **Bank Integration** (General banking - 1 issue)

---

## 🎯 2026 Project Priorities (Based on 2025 Data)

### Continue Heavy Investment

**Card Manager** (30.1% of effort):
- Maintain as primary focus
- Mature the platform
- Add advanced features

**Fiba Integration** (6.4%):
- Banking partnership critical
- Continue integration work
- Expand capabilities

### Grow & Mature

**Portal & Credit** (7.5% combined):
- Increase investment
- Customer-facing importance
- Feature parity

### Maintain & Optimize

**Supporting Services** (Gateway, Member, OTP, etc.):
- Keep operational
- Incremental improvements
- Stability focus

---

## 📞 Summary

**Service Banking Team** operates **13 microservices** with primary focus on **Card Manager** (30% of effort). Strong **quality culture** (31% QA work) and clear **architectural separation**. Good **Jira-GitLab alignment** enables traceability.

**2026 Recommendation:** Maintain card focus while growing portal/credit services. Continue quality-first approach.

---

*Data extracted from: 1,000 Jira issues (TSB project)*
*Analysis date: 2026-01-20*
*Method: Keyword analysis from issue summaries*
