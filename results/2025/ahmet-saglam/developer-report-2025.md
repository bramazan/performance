# Ahmet Sağlam - Performans Değerlendirme Raporu 2025

**Pozisyon:** QA Engineer - Fiziki POS Versiyon Test & Yayılım
**Tarih:** 20 Ocak 2026
**Değerlendirme Dönemi:** Şubat 2025 - Ocak 2026

---

## Özet

Ahmet Sağlam, Payment ekibinde fiziki POS terminal versiyonlarının test süreçleri ve saha yayılımından sorumlu olarak görev yapmaktadır. TPAY board'undaki verilere göre 41 task üzerinde çalışmış ve **%61 Done Rate** başarı oranı göstermiştir.

⚠️ **KRİTİK UYARI:** 12 aylık değerlendirme döneminde toplam 41 task (gerçek iş: 22 task, aylık ortalama: **1.8 task/ay**) **ciddi şekilde düşüktür**. QA Engineer pozisyonu için beklenen aylık 8-15 task seviyesinin **çok altında** performans gösterilmiştir.

---

## Genel Metrikler

| Metrik | Değer | Yüzde |
|--------|-------|-------|
| **Toplam Task Sayısı** | 41 | 100% |
| **Gerçek İş Task'ları** | 22 | 53.7% |
| **Rutin/Admin Task'lar** | 19 | 46.3% |
| **Tamamlanan (Done + Closed)** | 25 | **61.0%** |
| **Devam Eden (In Progress)** | 3 | 7.3% |
| **Bekleyen (Backlog)** | 13 | 31.7% |

### Aylık Performans Analizi (12 aylık dönem)
| Metrik | Değer | Beklenti | Durum |
|--------|-------|----------|--------|
| **Aylık Toplam Task** | 3.4 task/ay | - | - |
| **Aylık Gerçek İş** | **1.8 task/ay** | 8-15 task/ay | 🔴 **Çok Düşük** |
| **QA Engineer Standart** | - | 8-15 task/ay | - |
| **Developer Standart** | - | 10-20 task/ay | - |

⚠️ **Performans Açığı:** Ahmet'in aylık gerçek iş yükü (1.8 task) beklentinin **~80% altında**

### Done Rate Analizi
- ✅ **Done:** 19 task (%46.3)
- ✅ **Closed:** 6 task (%14.6)
- ⏳ **In Progress:** 3 task (%7.3)
- 📋 **Backlog:** 13 task (%31.7)

**Başarı Oranı:** %61.0 (Done + Closed)

---

## Task Tipi Dağılımı

Ahmet'in çalışma alanları şu şekilde dağılmaktadır:

| Task Tipi | Sayı | Yüzde | Açıklama |
|-----------|------|-------|----------|
| **Operation** | 10 | 24.4% | Operasyonel işlemler, yayılım süreçleri |
| **Meeting** | 9 | 22.0% | Toplantı katılımları |
| **Testing** | 8 | 19.5% | Ana test görevleri |
| **Test** | 6 | 14.6% | Test subtask'ları |
| **Story** | 4 | 9.8% | Kullanıcı hikayeleri |
| **Cross Check** | 1 | 2.4% | Çapraz kontrol |
| **Development** | 1 | 2.4% | Geliştirme |
| **Task** | 1 | 2.4% | Genel görev |
| **Epic** | 1 | 2.4% | Epic seviye iş |

### Değerlendirme
- **Test odaklı çalışma:** Test ve Testing görevleri toplamda **%34.1** oranında (14 task)
- **Operasyonel sorumluluk:** Operation task'ları **%24.4** ile önemli bir yer tutuyor
- **Toplantı yoğunluğu:** Meeting task'ları **%22.0** ile oldukça yüksek

---

## Priority Dağılımı

| Priority | Sayı | Yüzde |
|----------|------|-------|
| **Lowest** | 36 | 87.8% |
| **High** | 2 | 4.9% |
| **Kritik** | 1 | 2.4% |
| **Medium** | 1 | 2.4% |
| **Highest** | 1 | 2.4% |

**Not:** Task'ların çoğunluğu (%87.8) "Lowest" priority olarak işaretlenmiş. Bu, rutin test ve operasyon işlerinin doğası gereği normaldir.

---

## Bug ve Dokümantasyon Analizi

| Kategori | Sayı | Oran |
|----------|------|------|
| **Bug Task** | 0 | 0.0% |
| **Dokümantasyon Task** | 0 | 0.0% |

### Değerlendirme
- Ahmet'in task'larında doğrudan "Bug" kategorisinde iş bulunmuyor
- QA rolünde bug tespiti yapıyor ancak bug fix'e odaklanmıyor (doğru yaklaşım)
- Dokümantasyon görevi bulunmuyor - bu iyileştirme alanı olabilir

---

## Öne Çıkan Başarılı Projeler

### ✅ Tamamlanan Kritik İşler

#### 1. SSL Sertifika Güncellemeleri ve Yayılımı
- **[TPAY-1228]** 1.2.22 SSL versiyon Release Saha Yayılımı - ✅ Done
- **[TPAY-1160]** 1.2.22 SSL versiyon Release Saha Yayılımı - ✅ Done
- **[TPAY-1046]** Yeni SSL sertifika PROD Test - ✅ Done

**Etki:** Güvenlik sertifikalarının güncellenmesi kritik bir iş olup başarıyla tamamlanmış.

#### 2. Versiyon Yayılımları
- **[TPAY-1050]** Paratika-Garanti-EmlakKatılım-Tami 1.2.22 Versiyon yayılımı - ✅ Done
- **[TPAY-1161]** WhiteLabel - Entegrasyon Firmaları için Versiyon Release - ✅ Done
- **[TPAY-975]** 1.2.22 Uzaktan yükleme Testleri ve Yayılımı - ✅ Done
- **[TPAY-713]** 1.2.20 Uzaktan yükleme Testleri ve Yayılımı - ✅ Closed

**Etki:** Birden fazla banka entegrasyonunda (Paratika, Garanti, Emlak Katılım, Tami) başarılı versiyon yayılımı.

#### 3. Kritik Test Senaryoları
- **[TPAY-1007]** Yapılacak olan testler - ✅ Done
  - Ortak Pos 1.7.28_9, Techpos 2.1.6_7 versiyonları
  - QR işlem onay kodu sorunları
  - Garanti, Tami, Paratika, Emlak Katılım test süreçleri
- **[TPAY-145]** Smart POS - gün sonu testi (Highest Priority) - ✅ Done
- **[TPAY-141]** Android cihazlarda logout durumları - ✅ Done
- **[TPAY-289]** Terminal-Ödeal uyumsuzluk durumları - ✅ Done

**Etki:** İş kritik senaryoların test edilmesi ve sistem güvenilirliğinin artırılması.

### 📋 Backlog'da Bekleyen İş
- **[TPAY-1449]** test - smartPos larda Ip-Port eklenmesinin testleri - Kritik Priority

---

## Çalışma Alanları

### 1. Fiziki POS Terminal Testleri
- SSL sertifika güncellemeleri
- Versiyon yükleme ve uzaktan yayılım testleri
- Gün sonu işlemleri
- Terminal-backend senkronizasyon testleri

### 2. Multi-Bank Entegrasyonları
- Garanti
- Paratika
- Emlak Katılım
- Tami

### 3. Cihaz Testleri
- SmartPOS cihazlar
- Android tabanlı POS'lar
- PAX A80, PAX A6650, PAX IM30 gibi farklı model testleri

---

## Güçlü Yönler

1. ✅ **Versiyon Yayılımında Uzmanlık**
   - Birden fazla banka entegrasyonunda başarılı release yönetimi
   - SSL güvenlik güncellemelerini başarıyla yönetmiş

2. ✅ **Test Senaryosu Çeşitliliği**
   - SmartPOS, Android, farklı POS modellerinde deneyim
   - Kritik senaryoları (gün sonu, logout, vb.) başarıyla test etmiş

3. ✅ **Operasyonel Sorumluluk**
   - Sadece test değil, yayılım süreçlerini de yönetiyor
   - Operation task'larında yüksek başarı oranı

4. ✅ **Kritik İşlerde Başarı**
   - Highest ve High priority işlerde %100 tamamlanma
   - SSL gibi güvenlik kritik konularda başarı

---

## İyileştirme Alanları

### 🔴 KRİTİK SORUNLAR

1. **🚨 TASK SAYISI ÇOK DÜŞÜK - EN ÖNEMLİ SORUN**
   - **Mevcut:** 1.8 gerçek task/ay
   - **Beklenti:** 8-15 task/ay (QA Engineer standart)
   - **Açık:** %80 performans açığı
   - **Etki:** Ekip kapasitesinin çok altında çalışma
   - **Acil Aksiyon Gerekli:**
     - Task alma oranını 4-5 kat artırmak
     - Sprint'lere daha fazla iş almak
     - Backlog'dan aktif olarak task çekmek
     - Proaktif olarak yeni test alanları belirlemek

2. ⚠️ **Backlog Yönetimi**
   - 13 task (%31.7) backlog'da bekliyor
   - Bazı task'lar uzun süredir backlog'da (Meeting ve Operation subtask'ları)
   - **Öneri:** Backlog task'larını önceliklendirip temizlemek

3. ⚠️ **Dokümantasyon Eksikliği**
   - Test süreçleri ve yayılım dokümanları task olarak görünmüyor
   - **Öneri:** Test senaryoları, yayılım prosedürleri için dokümantasyon task'ları oluşturulmalı

4. ⚠️ **Meeting Task'larının Yüksekliği**
   - Meeting task'ları %22 oranında
   - Birçoğu backlog'da
   - **Öneri:** Meeting task'larının gerekliliğini gözden geçirmek

5. ⚠️ **Task Detaylarının Eksikliği**
   - Bazı task'ların açıklaması (description) boş
   - **Öneri:** Task'lara detaylı açıklama eklemek, ileride referans için faydalı olacaktır

---

## Performans Skoru

| Kategori | Puan | Açıklama |
|----------|------|----------|
| **🔴 Task Hacmi/Verimlilik** | **2/10** | **1.8 task/ay (Beklenti: 8-15) - KRİTİK DÜŞÜK** |
| **Task Tamamlama Oranı** | 8/10 | %61 done rate kabul edilebilir |
| **Kritik İşlerde Başarı** | 10/10 | High/Highest priority işlerde %100 başarı |
| **Test Kapsamı** | 9/10 | Geniş cihaz ve entegrasyon test kapsamı |
| **Operasyonel Yönetim** | 9/10 | Yayılım süreçlerini başarıyla yönetiyor |
| **Dokümantasyon** | 4/10 | Dokümantasyon task'ı bulunmuyor |
| **Backlog Yönetimi** | 6/10 | Backlog task oranı yüksek |

**Genel Performans Skoru:** **5.4/10** 🔴

⚠️ **Genel değerlendirme düşük çıkmıştır.** Kalite yüksek ancak **miktar ciddi şekilde yetersizdir**.

---

## Öneriler

### Kısa Vadeli (1-2 ay)
1. Backlog'daki 13 task'ı önceliklendirip azaltmak
2. In Progress olan 3 task'ı tamamlamaya odaklanmak
3. Kritik priority olan TPAY-1449 (IP-Port testleri) task'ını ivedilikle tamamlamak

### Orta Vadeli (3-6 ay)
1. Test senaryolarını dokümante etmek için task'lar oluşturmak
2. Yayılım prosedürlerini standartlaştırmak ve dokümante etmek
3. Meeting task'larını azaltmak veya daha verimli hale getirmek

### Uzun Vadeli (6-12 ay)
1. Otomatize test senaryoları geliştirmeye başlamak
2. Test coverage metriklerini takip etmeye başlamak
3. Cross-team collaboration için dokümantasyon altyapısı kurmak

---

## Sonuç

### 🔴 KRİTİK DEĞERLENDİRME

Ahmet Sağlam'ın performansı **yetersizdir** ve **acil iyileştirme gerektirir**.

#### Olumlu Yönler (Kalite)
- ✅ SSL güncellemeleri gibi kritik güvenlik işlerini başarıyla tamamlamış
- ✅ Birden fazla banka entegrasyonunda versiyon yayılımlarını yönetmiş
- ✅ Geniş cihaz ve test senaryosu kapsamında çalışmış
- ✅ Tamamladığı işlerde %100 başarı oranı (kritik priority'lerde)

#### 🚨 Kritik Sorunlar (Miktar)
- 🔴 **TASK SAYISI ÇOK DÜŞÜK:** 1.8 task/ay (Beklenti: 8-15 task/ay)
- 🔴 **%80 PERFORMAance AÇIĞI:** Ekip standartlarının çok altında
- 🔴 **12 AYDA SADECE 22 GERÇEK İŞ:** Kabul edilemez düşük
- ⚠️ Backlog yönetimi yetersiz (%31.7 backlog)
- ⚠️ Dokümantasyon eksikliği
- ⚠️ Meeting yoğunluğu (%22)

### Nihai Karar

**Performans Durumu:** 🔴 **YETERSİZ** (5.4/10)

**Kalite vs Miktar:**
- **Kalite:** İyi (tamamlanan işlerde başarılı)
- **Miktar:** Çok düşük (1.8 task/ay, beklentinin %20'si)

**Aksiyon Planı:**
1. **ACİL (1 ay içinde):** Task alma oranını minimum 6-8 task/ay'a çıkarmak
2. **ORTA VADE (2-3 ay):** 10-12 task/ay hedefine ulaşmak
3. **Sürekli:** Backlog'u temizlemek ve sprint commitment'larını artırmak

**Öneri:** Performance Improvement Plan (PIP) başlatılması ve aylık takip ile performans artışı sağlanması önerilir.

---

**Rapor Tarihi:** 20 Ocak 2026
**Hazırlayan:** Claude Code Performance Analysis
**Veri Kaynağı:** Jira TPAY Board 212
