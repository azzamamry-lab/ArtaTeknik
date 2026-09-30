# Website ARTA TEKNIK

Website jasa **servis AC & pemasangan CCTV** untuk wilayah **Solo, Sukoharjo, Karanganyar**.

## 🌐 Link

- **Live (sementara):** https://azzamamry-lab.github.io/ArtaTeknik/
- **Domain target:** https://artatehnik.com (belum dibeli)

## 📄 Struktur Halaman

| Halaman | URL | Isi |
|---|---|---|
| Beranda | `/` | Hero, 3 layanan, keunggulan, 3 area, FAQ, CTA |
| Servis AC | `/layanan/servis-ac.html` | Masalah, pekerjaan, FAQ khusus |
| Pasang AC | `/layanan/pasang-ac.html` | Masalah, pekerjaan, FAQ khusus |
| Pasang CCTV | `/layanan/pasang-cctv.html` | Masalah, pekerjaan, FAQ khusus |
| Solo | `/area/solo.html` | 5 kecamatan, layanan, FAQ area |
| Sukoharjo | `/area/sukoharjo.html` | 12 kecamatan, layanan, FAQ area |
| Karanganyar | `/area/karanganyar.html` | 12 kecamatan, layanan, FAQ area |
| Kontak | `/kontak.html` | 3 cara hubungi, langkah pesan, FAQ |

**Total: 8 halaman + robots.txt + sitemap.xml**

## 🔧 Cara Kerja

Konten dihasilkan dari **satu file data** (`data.yaml`):

```bash
python build.py
```

Ubah `data.yaml`, jalankan `build.py`, semua halaman ikut berubah.
Tidak perlu edit HTML satu per satu.

## 🔍 SEO yang Sudah Diterapkan

### Teknis
- ✅ **Meta description** unik per halaman
- ✅ **Canonical tag** (hindari konten duplikat)
- ✅ **Open Graph** 7 tag (preview bagus di WA/FB/LinkedIn)
- ✅ **Twitter Card** 4 tag
- ✅ **robots.txt** dengan izin AI crawler
- ✅ **sitemap.xml** 8 URL
- ✅ **Mobile-friendly** (sudah diuji di 390px, tanpa overflow)
- ✅ **Semantic HTML** (header, nav, section, article, footer)

### Schema.org (20 schema, semua valid)
| Halaman | Schema |
|---|---|
| Beranda | `HVACBusiness` + `FAQPage` |
| Layanan | `Service` + `BreadcrumbList` + `FAQPage` |
| Area | `BreadcrumbList` + `FAQPage` |
| Kontak | `BreadcrumbList` + `FAQPage` |

### SEO Lokal (yang paling penting untuk jasa)
- ✅ **Halaman terpisah per area** (Solo, Sukoharjo, Karanganyar)
- ✅ **Kecamatan disebut lengkap** (29 kecamatan total)
- ✅ **Judul menyebut kota** ("Jasa Servis AC Solo, Sukoharjo, Karanganyar")
- ✅ **areaServed** di schema
- ✅ **Nama kecamatan di konten** (bukan cuma di meta)

### GEO (Generative Engine Optimization)
Biar muncul di ChatGPT, Gemini, Perplexity:
- ✅ **robots.txt** mengizinkan GPTBot, PerplexityBot, ClaudeBot, dll
- ✅ **FAQ terstruktur** (schema FAQPage) — AI suka format tanya-jawab
- ✅ **Jawaban langsung** di setiap FAQ (tidak bertele-tele)
- ✅ **Data faktual** (nama kecamatan, jam kerja, area layanan)
- ✅ **Entity jelas** (`HVACBusiness` dengan nama, telepon, area)

## 🎨 Desain

| Warna | Kode | Dipakai |
|---|---|---|
| Navy | `#0b2a4e` | Header, hero, footer |
| Blue | `#1c5fb0` | Aksen, link, ikon |
| Gold | `#f4b400` | Tombol utama, highlight |
| Green | `#25d366` | Tombol WhatsApp |
| Sky | `#f2f7fd` | Latar section |

Font: **Plus Jakarta Sans**

## 🔜 Langkah Berikutnya

1. **Beli domain** `artatehnik.com` (~Rp 130-180rb/tahun)
2. **Set DNS** ke GitHub Pages (saya bantu)
3. **Aktifkan HTTPS** (otomatis di GitHub Pages)
4. **Daftar Google Business Profile** (penting untuk SEO lokal)
5. **Submit sitemap** ke Google Search Console

## 📝 Yang Perlu Dilengkapi

- [ ] Foto asli pekerjaan (untuk galeri)
- [ ] Testimoni pelanggan asli
- [ ] Harga mulai (kalau mau ditampilkan)
- [ ] Google Maps embed (butuh alamat usaha)
- [ ] Form kontak (butuh layanan email/backend)
