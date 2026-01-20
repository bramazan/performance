# 🚨 KRİTİK BULGU: Alican İnan - Ekip Kültürü Etkisi

**Tarih:** 2026-01-20
**Analyst:** GitLab DORA Metrics Tool

---

## 🎯 Executive Summary

**Alican İnan'ın MR kullanımındaki düşüş individual bir problem DEĞİL, Service Banking ekibinin team culture'ından kaynaklanıyor.**

### Sayılar

| Metric | Payment Team (Mar-Jul) | Service Banking (Aug-Dec) | Change |
|--------|------------------------|---------------------------|---------|
| **MR Usage** | **93.8%** ⭐ | **16.6%** 🚨 | **-77.2pp** |
| MRs | 15 | 45 | +30 |
| Direct Commits | 1 | 226 | +225 |
| Total Work | 16 | 271 | +255 |

---

## 📊 Aylık Detay Breakdown

### Payment Period (Excellent MR Usage)

| Month | MRs | Commits | Total | MR % | Status |
|-------|-----|---------|-------|------|--------|
| Mar | 2 | 0 | 2 | 100% | ⭐ Perfect |
| Apr | 3 | 0 | 3 | 100% | ⭐ Perfect |
| May | 5 | 0 | 5 | 100% | ⭐ Perfect |
| Jun | 1 | 0 | 1 | 100% | ⭐ Perfect |
| Jul | 2 | 1 | 3 | 66.7% | ✅ Good |

**Payment Average: 93.8% MR Usage** ⭐

### Service Banking Period (Critical Drop)

| Month | MRs | Commits | Total | MR % | Status |
|-------|-----|---------|-------|------|--------|
| Aug | 6 | 35 | 41 | 14.6% | 🚨 Critical |
| Sep | 2 | 69 | 71 | 2.8% | 🚨 Critical |
| Oct | 10 | 51 | 61 | 16.4% | 🚨 Critical |
| Nov | 17 | 31 | 48 | 35.4% | 🚨 Critical |
| Dec | 12 | 40 | 52 | 23.1% | 🚨 Critical |

**Service Banking Average: 16.6% MR Usage** 🚨

---

## 💡 Root Cause Analysis

### ❓ Neden Service Banking'de bu kadar düşük?

#### 1. **EKİP KÜLTÜRÜ FARKI** (Primary Cause)

Payment Team:
- MR-first culture
- Code review mandatory
- Alican adapte olmuş ve MÜKEMMELuygulamış (%93.8)

Service Banking Team:
- Direct commit culture
- Peer review optional/rare
- Alican ekip normlarına uyum sağlamış (ama yanlış yönde)

**Kanıt:** Aynı Service Banking ekibinde:
- Mert Kaim: 86.7% MR usage ⭐ (EXCELLENT)
- Alican İnan: 16.6% MR usage 🚨 (CRITICAL)

→ **Ekip içinde standardizasyon YOK!**

#### 2. **HIZLI DELIVERY BASKISI**

Service Banking'de:
- 226 commit in 5 months = günde ~1.5 commit
- Çok hızlı iteration
- Direct commit = faster (ama code quality sacrifice)

#### 3. **ONBOARDİNG GAP**

- Yeni ekibe katıldığında process training eksik olabilir
- Existing team members'ı follow etmiş (yanlış pattern)
- Code review culture transfer edilmemiş

---

## 🔍 Production Impact Analysis

### Merge Status

- **Total MRs:** 60
- **Merged:** ~85% (estimated based on "merged" state)
- **In Production:** High rate (MR'lar genelde merge ediliyor)

### Production Pathways

| Path | Count | % of Total | Risk Level |
|------|-------|------------|------------|
| **Via MRs (reviewed)** | ~51 MRs | ~18% | ✅ Low - Peer reviewed |
| **Via Direct Commits** | 227 commits | ~79% | 🚨 HIGH - No review! |
| **Work in Progress** | ~9 MRs | ~3% | - |

**→ Production kod'un %79'u code review bypass etti!** 🚨

---

## 🆚 Service Banking Team Internal Comparison

### Mert vs Alican (Same Team, Different Practices)

| Metric | Mert Kaim | Alican İnan | Winner |
|--------|-----------|-------------|--------|
| **MR Usage** | 86.7% | 16.6% | Mert (5x better!) |
| **Total Work** | 188 | 271 | Alican (+44% volume) |
| **Bug Ratio** | 12.3% | 29.5% | Mert (2.4x better quality) |
| **Code Reviews Given** | 319 | 239 | Mert (+33% collaboration) |

**Trade-off:**
- Alican: Higher speed, lower quality, less review
- Mert: Lower volume, higher quality, more review

**Sustainable:** Mert's approach (industry best practice)

---

## 🚨 Critical Issues Identified

### 1. **Team Process Inconsistency**

Service Banking ekibinde:
- Herkes kendi workflow'unu kullanıyor
- Standardizasyon yok
- Code review culture zayıf

### 2. **Quality Control Gap**

- %79 production code = no peer review
- Bug ratio yüksek (%25-29%)
- Technical debt accumulation riski

### 3. **Knowledge Silos**

- Direct commit = team doesn't see the changes
- No knowledge sharing through MR discussions
- Bus factor riski (Alican hastalansa, kimse bilmez)

---

## ✅ Pozitif Bulgular

### Alican CAN Use MRs!

Payment ekibinde gösterdi:
- %93.8 MR usage (industry elite level)
- Process'e uyum sağlayabiliyor
- Capability var, execution environment'a bağlı

### High Productivity

- 271 work items in 5 months (Service Banking)
- Active developer
- High output (even if process needs improvement)

---

## 🎯 Recommendations

### 1. **URGENT: Team-Level Process Standardization**

**Priority: CRITICAL**

Service Banking ekibi için:

- [ ] MR workflow'u **MANDATORY** yap
- [ ] Code review'ı required yap (min 1 approval)
- [ ] Mert'i process champion yap (exemplar)
- [ ] Team retro: process discussion

**Timeline:** Başlangıç: Immediately | Full adoption: Q1 2026

### 2. **Individual Coaching for Alican**

**Priority: HIGH**

- [ ] 1-on-1 with Team Lead
- [ ] "You did it perfectly in Payment! Why change?"
- [ ] Weekly check-ins: MR usage tracking
- [ ] Pair programming with Mert (1-2 weeks)

**Goal:** Return to 80%+ MR usage by end of Q1 2026

### 3. **CI/CD Enforcement**

**Priority: MEDIUM**

Technical controls:
- [ ] Branch protection: require MR for main
  - Disable direct push to main/master
- [ ] Pre-commit hooks: remind about MR creation
- [ ] GitHub Actions/GitLab CI: auto-comment on direct commits

**Timeline:** Q1 2026

### 4. **Team Metrics Dashboard**

**Priority: MEDIUM**

Weekly team dashboard:
- Individual MR usage %
- Code review participation
- Bug fix ratio
- Public visibility (healthy competition)

**Timeline:** Q2 2026

---

## 📈 Expected Outcomes

### If Recommendations Implemented:

**Q1 2026:**
- Alican MR usage: 16.6%  → 60%+ (conservative)
- Team average MR usage: 51%+ (Mert 87% + Alican 60% / 2)

**Q2 2026:**
- Alican MR usage: 80%+ (back to Payment levels)
- Bug ratio: 25% → <15%
- Code review culture: Established

**Q3 2026:**
- Sustainable team practices
- Knowledge sharing improved
- Quality metrics improved

---

## 💬 Key Takeaways

### For Alican:

> "You're not the problem. Payment'ta mükemmeldin (%93.8 MR usage). Service Banking'de ekip normlarına uyum sağladın - ama yanlış normlara. Capability'n kanıtlanmış, sadece Payment'taki practices'e dön!"

### For Service Banking Team:

> "Ekip seviyesinde process standardizasyonu kritik. Mert best practice'leri uyguluyor (%86.7 MR), Alican'ın da Payment'ta gösterdiği gibi (%93.8). **Ekip normunu Mert seviyesine çıkarın!**"

### For Management:

> "Bu individual bir performance sorunu DEĞİL, team culture sorunu. Payment ekibi doğru yapıyor, Service Banking ekibi process'i benimsememiş. Solution: Team-level intervention, individual değil."

---

## 📊 Action Owner Matrix

| Action | Owner | Support | Deadline |
|--------|-------|---------|----------|
| **Process Documentation** | Team Lead | Mert (expert) | 2 weeks |
| **Branch Protection Setup** | DevOps | Team Lead | 1 week |
| **Alican 1-on-1** | Team Lead | - | Immediate |
| **Team Retro** | Team Lead | All team | 1 week |
| **Weekly Check-ins** | Team Lead | Alican | Ongoing |
| **Pair Programming** | Mert & Alican | Team Lead | 2 weeks |
| **Metrics Dashboard** | DevOps | Team Lead | 1 month |

---

**Conclusion:** Alican'ın "low MR usage" sorunu aslında **Service Banking team culture'ının bir semptom**u. Payment'ta mükemmel performans gösterdi, capability var. Solution: **Team-level process enforcement + Alican'a Payment habits'e dönüş desteği.**

---

*Analysis Date: 2026-01-20*
*Analyst: GitLab DORA Metrics Tool*
*Data Sources: gitlab_user_metrics, team_lead_analysis*
