# Panduan Beli Domain & Setting DNS — ARTA TEKNIK

Domain yang akan dibeli: **`artatehnik.com`** ✅ (tersedia, sudah dicek)

---

## Langkah 1: Beli Domain

Pilih salah satu registrar:

### Opsi A: Cloudflare (termurah jangka panjang) ⭐
1. Buka https://dash.cloudflare.com/sign-up
2. Daftar akun (gratis)
3. Menu kiri → **Domain Registration** → **Register Domains**
4. Cari `artatehnik.com`
5. Bayar **~$10,44/tahun** (~Rp 170rb) pakai kartu kredit/debit

**Kelebihan:** harga asli tanpa markup, perpanjangan murah, DNS tercepat, HTTPS otomatis

### Opsi B: Rumahweb (bayar transfer bank Indonesia)
1. Buka https://www.rumahweb.com/domain-murah/
2. Cari `artatehnik.com`
3. Bayar **~Rp 130rb/tahun** via transfer bank / e-wallet / QRIS

**Kelebihan:** Bahasa Indonesia, support lokal, bisa transfer bank

### Opsi C: Niagahoster
1. Buka https://www.niagahoster.co.id/domain-murah
2. Cari `artatehnik.com`
3. Bayar **~Rp 150rb/tahun**

---

## Langkah 2: Setting DNS

Setelah beli, **kirim ke saya**: "domain sudah dibeli" + nama registrar.

Saya akan kasih **record DNS persis** yang perlu kamu isi.

### Record yang akan saya minta kamu isi

**Untuk domain utama (`artatehnik.com`) — 4 record A:**

| Type | Name | Value | TTL |
|---|---|---|---|
| A | `@` | `185.199.108.153` | Auto |
| A | `@` | `185.199.109.153` | Auto |
| A | `@` | `185.199.110.153` | Auto |
| A | `@` | `185.199.111.153` | Auto |

**Untuk `www` — 1 record CNAME:**

| Type | Name | Value | TTL |
|---|---|---|---|
| CNAME | `www` | `azzamamry-lab.github.io` | Auto |

*(IP di atas adalah IP resmi GitHub Pages — stabil, jarang berubah.)*

---

## Langkah 3: Yang Saya Kerjakan Setelah DNS Aktif

| # | Tugas | Waktu |
|---|---|---|
| 1 | Tambah file `CNAME` ke repo | 1 menit |
| 2 | Setting custom domain di GitHub Pages | 2 menit |
| 3 | Aktifkan **HTTPS** (Let's Encrypt gratis) | 5 menit |
| 4 | Ganti canonical URL dari placeholder ke domain asli | 2 menit |
| 5 | Update sitemap.xml | 1 menit |
| 6 | Update robots.txt | 1 menit |
| 7 | Verifikasi semua halaman lewat domain baru | 5 menit |

**Total: ~20 menit.** Tinggal bilang saja.

---

## ⏱️ Berapa Lama DNS Aktif?

| Tahap | Waktu |
|---|---|
| Propagasi DNS | 5 menit - 24 jam (biasanya **15-30 menit**) |
| GitHub baca domain | 1-10 menit |
| HTTPS aktif | 5-60 menit |
| **Total realistik** | **~1 jam** |

---

## 📋 Checklist Setelah Domain Aktif

- [ ] `artatehnik.com` bisa dibuka
- [ ] `www.artatehnik.com` bisa dibuka
- [ ] HTTPS (gembok hijau) aktif
- [ ] URL lama GitHub redirect ke domain baru
- [ ] Canonical URL sudah domain baru
- [ ] Sitemap sudah domain baru

---

## 🎯 Setelah Domain Aktif — Langkah SEO Berikutnya

Yang **paling penting** untuk jasa lokal:

### 1. Google Business Profile (WAJIB) ⭐⭐⭐
Ini yang bikin kamu muncul di **Google Maps** + pencarian lokal.
- Buka https://business.google.com
- Daftar dengan nama **ARTA TEKNIK** (harus sama persis dengan website)
- Isi alamat, jam kerja, nomor WA
- Upload foto pekerjaan
- **Kunci: nama harus SAMA PERSIS** di website, GBP, sosmed → ini yang bikin AI percaya

### 2. Google Search Console
- Buka https://search.google.com/search-console
- Tambah properti `artatehnik.com`
- Submit sitemap: `artatehnik.com/sitemap.xml`
- Ini bikin Google cepat mengindeks

### 3. Konsistensi NAP (Name, Address, Phone)
Pastikan **sama persis** di:
- Website ✅ (sudah)
- Google Business Profile
- Facebook Page
- Instagram Bio
- Direktori lokal (Google Maps, Waze, dll)

**Alasan:** AI & Google cek konsistensi dari banyak sumber. Kalau beda-beda, kepercayaan turun.

---

## 💰 Ringkasan Biaya

| Item | Biaya |
|---|---|
| Domain `.com` | Rp 130rb - 180rb / tahun |
| Hosting (GitHub Pages) | **Gratis** |
| HTTPS (Let's Encrypt) | **Gratis** |
| **Total** | **~Rp 180rb/tahun** |

---

## ❓ Kalau Ada Pertanyaan

**"Kenapa tidak sekalian beli hosting?"**
Tidak perlu. GitHub Pages gratis, cepat, dan sudah pakai CDN global. Website-mu statis (HTML), jadi tidak butuh server.

**"Kalau nanti mau tambah form kontak?"**
Bisa pakai layanan gratis seperti Formspree, atau Cloudflare Workers. Nanti saya bantu.

**"Apakah perlu beli domain lain juga?"**
Tidak wajib. Tapi kalau mau aman, bisa beli `artateknik.com` (ejaan KBBI) lalu redirect ke yang utama — supaya orang yang salah tulis tetap sampai. Biaya tambahan ~Rp 170rb/tahun.
