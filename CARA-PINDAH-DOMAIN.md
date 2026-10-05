# Cara Pindah ke Domain artatehnik.com (1 Langkah)

Setelah domain **artatehnik.com** dibeli dan DNS diarahkan ke GitHub Pages,
cukup ubah **1 baris** di `build.py`, lalu build + push:

```bash
cd C:/Users/HI/arta-website
# 1. Buka build.py, ubah baris DOMAIN:
#    DARI: DOMAIN = "https://azzamamry-lab.github.io/ArtaTeknik"
#    JADI: DOMAIN = "https://artatehnik.com"
python build.py          # regenerate 10 file
python cek_seo.py        # pastikan semua masih valid
git add -A
git -c user.name="azzamamry-lab" -c user.email="azzamamry@gmail.com" commit -m "Pindah ke domain artatehnik.com"
git push origin main
```

Selesai. Canonical, sitemap, robots, og:image, dan schema otomatis ikut pindah
karena semuanya mengambil dari variabel `DOMAIN`.

## Setting DNS di GitHub (setelah beli domain)

1. Buka repo: https://github.com/azzamamry-lab/ArtaTeknik/settings/pages
2. Di **Custom domain**, isi: `artatehnik.com` -> Save
3. GitHub otomatis bikin file `CNAME`. Centang **Enforce HTTPS**
4. Di panel registrar domain, tambahkan DNS record:

   | Type  | Name | Value                  |
   |-------|------|------------------------|
   | A     | @    | 185.199.108.153        |
   | A     | @    | 185.199.109.153        |
   | A     | @    | 185.199.110.153        |
   | A     | @    | 185.199.111.153        |
   | CNAME | www  | azzamamry-lab.github.io |

5. Tunggu 15 menit - 24 jam (propagasi DNS). Cek dengan: `nslookup artatehnik.com`

## Setelah domain aktif

- **Google Search Console**: https://search.google.com/search-console
  Tambahkan properti `artatehnik.com`, submit sitemap:
  `https://artatehnik.com/sitemap.xml`
  Kalau dapat kode verifikasi, tempel ke `GSC_VERIFIKASI = ""` di build.py.

- **Bing Webmaster Tools**: https://www.bing.com/webmasters
  (ini yang dipakai ChatGPT untuk cari data web, penting untuk GEO)

- **Google Business Profile**: pastikan nama & nomor WA **sama persis**
  dengan yang di website (kunci GEO).
