# -*- coding: utf-8 -*-
"""
Generator Website ARTA TEKNIK
=============================
Baca data.yaml -> hasilkan semua halaman HTML.

Struktur keluaran:
    index.html                    (beranda)
    layanan/servis-ac.html
    layanan/pasang-ac.html
    layanan/pasang-cctv.html
    area/solo.html
    area/sukoharjo.html
    area/karanganyar.html
    kontak.html
    robots.txt
    sitemap.xml

Jalankan:  python build.py
"""

import html
from pathlib import Path
from datetime import date

try:
    import yaml
except ImportError:
    raise SystemExit("Perlu pyyaml: pip install pyyaml")

BASE = Path(__file__).parent
DATA = yaml.safe_load((BASE / "data.yaml").read_text(encoding="utf-8"))
CSS = (BASE / "_css_asli.css").read_text(encoding="utf-8")

# Domain final (setelah beli). Sementara dipakai URL GitHub Pages yang SUDAH
# hidup, supaya Google bisa mengindeks sekarang juga.
DOMAIN = "https://azzamamry-lab.github.io/ArtaTeknik"
DOMAIN_FINAL = "https://artatehnik.com"

# Tag verifikasi Search Console (isi kalau sudah punya)
GSC_VERIFIKASI = ""

B = DATA["bisnis"]
WA = B["telepon_wa"]
WA_LINK = f"https://wa.me/{WA}?text="


def esc(t):
    return html.escape(str(t), quote=True)


def wa_pesan(pesan):
    from urllib.parse import quote
    return WA_LINK + quote(pesan)


# ============================================================
# CSS TAMBAHAN (untuk fitur baru: FAQ, breadcrumb, tabel harga)
# ============================================================
CSS_TAMBAHAN = """
/* ============================================================
   TAMBAHAN v2 — ARTA TEKNIK
   Disesuaikan dengan class LP asli (.container, .section, .btn)
   ============================================================ */

/* --- Layout dasar --- */
.section{padding:76px 0}
.section-abu{background:var(--sky);border-top:1px solid var(--sky-border);border-bottom:1px solid var(--sky-border)}
.section h2{font-size:clamp(26px,3.3vw,38px);color:var(--navy);line-height:1.2;
  margin-bottom:14px;font-weight:800;letter-spacing:-.6px}
.section-title p{color:var(--muted);font-size:16.5px}

/* --- Header (dibuat ulang) --- */
header{position:sticky;top:0;z-index:80;background:rgba(255,255,255,.97);
  backdrop-filter:blur(12px);border-bottom:1px solid var(--sky-border);
  transition:box-shadow .3s}
header.gulir{box-shadow:0 6px 24px rgba(11,42,78,.09)}
.bar{display:flex;align-items:center;justify-content:space-between;gap:18px;padding:14px 0}
.brand{display:flex;align-items:center;gap:11px;text-decoration:none}
.brand svg{width:40px;height:40px;flex-shrink:0}
.nm-brand{font-size:17.5px;font-weight:800;color:var(--navy);line-height:1.1;
  display:block;letter-spacing:.1px}
.sub-brand{font-size:9.5px;letter-spacing:1.4px;text-transform:uppercase;
  color:var(--blue);font-weight:700;display:block}
nav{display:flex;align-items:center;gap:24px}
nav a{color:var(--text);text-decoration:none;font-size:14.5px;font-weight:600;
  transition:color .2s}
nav a:hover,nav a.aktif{color:var(--blue)}
nav a.aktif{font-weight:700}
.menu-btn{display:none;background:var(--sky);border:1px solid var(--sky-border);
  border-radius:9px;padding:9px 13px;cursor:pointer;color:var(--navy);
  font-size:17px;line-height:1}

/* --- Hero kecil (halaman dalam) --- */
.hero-kecil{background:var(--grad-navy);color:#fff;padding:56px 0 52px;
  position:relative;overflow:hidden}
.hero-kecil::after{content:"";position:absolute;right:-180px;top:-140px;
  width:520px;height:520px;border-radius:50%;
  background:radial-gradient(circle,rgba(244,180,0,.16),transparent 68%)}
.hero-kecil .container{position:relative;z-index:2}
.hero-kecil h1{font-size:clamp(28px,3.8vw,44px);color:#fff;line-height:1.16;
  margin-bottom:16px;font-weight:800;letter-spacing:-.9px}
.hero-kecil .lede{color:rgba(255,255,255,.86);font-size:17px;max-width:680px;
  margin-bottom:28px}

/* --- Breadcrumb --- */
.breadcrumb{font-size:14px;color:rgba(255,255,255,.7);margin-bottom:18px}
.breadcrumb a{color:rgba(255,255,255,.9);text-decoration:none}
.breadcrumb a:hover{color:var(--gold)}
.breadcrumb span{margin:0 7px;opacity:.6}

/* --- Tombol tambahan --- */
.btn-wa{background:var(--green);color:#fff;box-shadow:0 10px 24px rgba(37,211,102,.34)}
.btn-wa:hover{background:#1eb955;transform:translateY(-2px)}
.btn-outline{background:transparent;color:var(--navy);border:1.5px solid var(--sky-border)}
.btn-outline:hover{background:var(--sky);border-color:var(--blue)}
.hero-kecil .btn-outline,.cta-akhir .btn-outline{color:#fff;border-color:rgba(255,255,255,.35)}
.hero-kecil .btn-outline:hover,.cta-akhir .btn-outline:hover{background:rgba(255,255,255,.12)}

/* --- Hero poin (grid 2x2 di kolom kanan hero) --- */
.hero-poin{display:grid;grid-template-columns:1fr 1fr;gap:14px}
.hp{background:rgba(255,255,255,.09);border:1px solid rgba(255,255,255,.17);
  border-radius:14px;padding:18px;backdrop-filter:blur(8px);
  transition:background .22s,border-color .22s}
.hp:hover{background:rgba(255,255,255,.14);border-color:rgba(244,180,0,.4)}
.hp b{display:block;color:#fff;font-size:14.5px;font-weight:700;margin-bottom:5px}
.hp span{color:rgba(255,255,255,.72);font-size:13px;line-height:1.5}
.mini-icons{display:flex;gap:22px;margin-top:28px;flex-wrap:wrap}
.mini-icons span{font-size:13.5px;color:rgba(255,255,255,.75);display:flex;
  align-items:center;gap:8px}
.mini-icons b{color:var(--gold);font-weight:700}

.hero-cta{display:flex;gap:13px;flex-wrap:wrap}

/* --- Hero poin (beranda) --- */
.hero-poin{display:grid;grid-template-columns:1fr 1fr;gap:16px}
.hp{background:rgba(255,255,255,.08);border:1px solid rgba(255,255,255,.16);
  border-radius:14px;padding:20px;backdrop-filter:blur(8px)}
.hp b{display:block;color:#fff;font-size:15px;font-weight:700;margin-bottom:5px}
.hp span{color:rgba(255,255,255,.75);font-size:13.5px;line-height:1.5}

/* --- Kartu layanan --- */
.kartu-layanan{display:grid;grid-template-columns:repeat(auto-fit,minmax(280px,1fr));
  gap:24px;max-width:1060px;margin:0 auto}
.kartu-l{background:#fff;border:1px solid var(--sky-border);border-radius:var(--radius);
  padding:32px 28px;transition:transform .22s,box-shadow .22s,border-color .22s;
  display:flex;flex-direction:column;box-shadow:var(--shadow)}
.kartu-l:hover{transform:translateY(-6px);box-shadow:var(--shadow-lg);border-color:var(--blue)}
.kartu-l .ikon{width:56px;height:56px;border-radius:15px;background:var(--sky);
  display:flex;align-items:center;justify-content:center;margin-bottom:18px}
.kartu-l h3{font-size:20px;color:var(--navy);margin-bottom:10px;font-weight:800}
.kartu-l p{color:var(--muted);font-size:15px;margin-bottom:20px;flex-grow:1;line-height:1.65}
.kartu-l .tautan{color:var(--blue);font-weight:700;text-decoration:none;font-size:15px;
  display:inline-flex;align-items:center;gap:7px;transition:gap .2s}
.kartu-l .tautan:hover{gap:12px}

/* --- Kartu area --- */
.area-grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(270px,1fr));
  gap:22px;max-width:1010px;margin:0 auto}
.area-kartu{background:#fff;border:1px solid var(--sky-border);border-radius:var(--radius);
  padding:28px;transition:transform .2s,box-shadow .2s;display:flex;flex-direction:column;
  box-shadow:var(--shadow)}
.area-kartu:hover{transform:translateY(-4px);box-shadow:var(--shadow-lg)}
.area-kartu h3{color:var(--navy);font-size:20px;margin-bottom:9px;font-weight:800}
.area-kartu p{color:var(--muted);font-size:14.5px;margin-bottom:14px;line-height:1.6}
.area-kartu .kec{font-size:13px;color:var(--muted);line-height:1.75;margin-bottom:18px;
  flex-grow:1}
.area-kartu .tautan{color:var(--blue);font-weight:700;text-decoration:none;font-size:14.5px;
  display:inline-flex;align-items:center;gap:7px;transition:gap .2s}
.area-kartu .tautan:hover{gap:12px}

/* --- Keunggulan --- */
.grid-keunggulan{display:grid;grid-template-columns:repeat(auto-fit,minmax(230px,1fr));
  gap:24px;max-width:1050px;margin:0 auto}
.keunggulan-item{text-align:center;padding:8px}
.keunggulan-ikon{width:58px;height:58px;border-radius:50%;background:var(--sky);
  display:flex;align-items:center;justify-content:center;margin:0 auto 16px;
  transition:background .24s,transform .24s}
.keunggulan-item:hover .keunggulan-ikon{background:var(--navy);transform:scale(1.08)}
.keunggulan-item:hover .keunggulan-ikon svg *{stroke:var(--gold)}
.keunggulan-item h3{font-size:17px;color:var(--navy);margin-bottom:8px;font-weight:700}
.keunggulan-item p{color:var(--muted);font-size:14.5px;line-height:1.65}

/* --- Blok rating Google --- */
.kotak-rating{display:grid;grid-template-columns:240px 1fr;gap:40px;
  align-items:center;background:#fff;border:1px solid var(--garis);
  border-radius:16px;padding:34px 40px}
.rating-kiri{text-align:center;border-right:1px solid var(--garis);padding-right:40px}
.rating-angka{font-size:64px;font-weight:800;color:var(--navy);line-height:1}
.rating-bintang{color:#f4b400;font-size:26px;letter-spacing:4px;margin:8px 0 4px}
.rating-label{font-size:13px;color:var(--muted);font-weight:600}
.rating-judul{font-size:26px;color:var(--navy);margin-bottom:12px;font-weight:800}
.rating-teks{color:var(--muted);font-size:15.5px;line-height:1.75;margin-bottom:22px}
.btn-review{display:inline-flex;align-items:center;gap:9px;
  background:var(--navy);color:#fff!important;text-decoration:none;
  padding:13px 22px;border-radius:10px;font-weight:700;font-size:14.5px;
  transition:transform .18s ease, box-shadow .18s ease}
.btn-review:hover{transform:translateY(-2px);box-shadow:0 8px 20px rgba(11,42,78,.25)}
.btn-review svg{color:#f4b400;flex:none}
@media (max-width:760px){
  .kotak-rating{grid-template-columns:1fr;gap:24px;padding:30px 24px}
  .rating-kiri{border-right:0;border-bottom:1px solid var(--garis);padding:0 0 24px}
  .rating-angka{font-size:52px}
  .rating-judul{font-size:21px}
}

/* --- Dua kolom (daftar) --- */
.dua-kolom{display:grid;grid-template-columns:1fr 1fr;gap:14px 32px;max-width:920px;
  margin:0 auto}
.dua-kolom ul{list-style:none;display:grid;gap:13px}
.dua-kolom li{display:flex;gap:12px;align-items:flex-start;font-size:15.5px;
  color:var(--text);line-height:1.6}
.dua-kolom li::before{content:"";width:20px;height:20px;flex-shrink:0;
  margin-top:3px;background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%2322c55e' stroke-width='3' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpath d='M4 12.5 9.5 18 20 6'/%3E%3C/svg%3E") no-repeat center/contain}
.dua-kolom a{color:var(--blue);text-decoration:none;font-weight:600}
.dua-kolom a:hover{text-decoration:underline}

/* --- FAQ --- */
.faq-list{max-width:880px;margin:0 auto}
.faq-item{background:#fff;border:1px solid var(--sky-border);border-radius:14px;
  margin-bottom:12px;overflow:hidden;transition:border-color .2s,box-shadow .2s}
.faq-item[open]{border-color:var(--blue);box-shadow:var(--shadow)}
.faq-item summary{cursor:pointer;padding:20px 24px;font-weight:700;font-size:16px;
  color:var(--navy);list-style:none;display:flex;justify-content:space-between;
  gap:18px;align-items:center;line-height:1.5;transition:color .2s}
.faq-item summary:hover{color:var(--blue)}
.faq-item summary::-webkit-details-marker{display:none}
.faq-item summary::after{content:"";width:22px;height:22px;flex-shrink:0;
  background:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231c5fb0' stroke-width='2.6' stroke-linecap='round'%3E%3Cpath d='M12 5v14M5 12h14'/%3E%3C/svg%3E") no-repeat center/contain;
  transition:transform .25s ease}
.faq-item[open] summary::after{background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 24 24' fill='none' stroke='%231c5fb0' stroke-width='2.6' stroke-linecap='round'%3E%3Cpath d='M5 12h14'/%3E%3C/svg%3E")}
.faq-item p{padding:18px 24px 24px;color:var(--muted);font-size:15.5px;line-height:1.75;
  border-top:1px solid var(--sky-border)}

/* --- Kotak info --- */
.kotak-info{background:var(--sky);border-left:4px solid var(--blue);
  border-radius:0 14px 14px 0;padding:22px 26px;margin:30px auto 0;max-width:920px}
.kotak-info p{margin:0;color:var(--text);font-size:15.5px;line-height:1.65}

/* --- Info kontak --- */
.info-kontak{display:grid;grid-template-columns:repeat(auto-fit,minmax(240px,1fr));
  gap:22px;max-width:920px;margin:0 auto}
.info-item{background:#fff;border:1px solid var(--sky-border);border-radius:var(--radius);
  padding:28px 24px;text-align:center;box-shadow:var(--shadow);
  transition:transform .2s}
.info-item:hover{transform:translateY(-4px)}
.info-item .ikon{width:52px;height:52px;border-radius:50%;background:var(--sky);
  display:flex;align-items:center;justify-content:center;margin:0 auto 15px}
.info-item h4{color:var(--navy);font-size:15px;margin-bottom:7px;font-weight:700}
.info-item p{margin:0;color:var(--muted);font-size:15px;line-height:1.6}
.info-item a{color:var(--blue);text-decoration:none;font-weight:700}
.info-item a:hover{text-decoration:underline}

/* --- CTA akhir --- */
.cta-akhir{background:var(--grad-navy);color:#fff;padding:76px 0;text-align:center;
  position:relative;overflow:hidden}
.cta-akhir::after{content:"";position:absolute;left:-160px;bottom:-180px;
  width:520px;height:520px;border-radius:50%;
  background:radial-gradient(circle,rgba(244,180,0,.14),transparent 68%)}
.cta-akhir .container{position:relative;z-index:2;max-width:700px}
.cta-akhir h2{color:#fff;font-size:clamp(25px,3.2vw,36px);margin-bottom:14px;
  font-weight:800;letter-spacing:-.7px}
.cta-akhir p{color:rgba(255,255,255,.85);font-size:16.5px;margin-bottom:32px}
.cta-tombol{display:flex;gap:13px;justify-content:center;flex-wrap:wrap}

/* --- Footer --- */
footer{background:var(--navy-3);color:rgba(255,255,255,.72);padding:52px 0 30px;
  font-size:14.5px}
.foot{display:grid;grid-template-columns:1.6fr 1fr 1fr 1.2fr;gap:34px;margin-bottom:34px}
.foot h4{color:#fff;font-size:14.5px;font-weight:700;margin-bottom:16px}
.foot ul{list-style:none;display:grid;gap:11px}
.foot a{color:rgba(255,255,255,.72);text-decoration:none;transition:color .2s}
.foot a:hover{color:var(--gold)}
.brand-foot{display:flex;align-items:center;gap:11px;margin-bottom:14px}
.nm-foot{font-size:17px;font-weight:800;color:#fff}
.foot-bottom{border-top:1px solid rgba(255,255,255,.13);padding-top:22px;
  display:flex;justify-content:space-between;gap:16px;flex-wrap:wrap;font-size:13.5px}

/* --- Responsif --- */
@media(max-width:980px){
  nav{display:none}
  nav.open{display:flex;flex-direction:column;align-items:stretch;gap:0;
    position:absolute;top:100%;left:0;right:0;background:#fff;
    border-bottom:1px solid var(--sky-border);padding:12px 24px 22px;
    box-shadow:0 16px 34px rgba(11,42,78,.13)}
  nav.open a{padding:15px 0;border-bottom:1px solid var(--sky-border)}
  nav.open a:last-of-type{border-bottom:none}
  nav.open .btn{margin-top:16px;width:100%}
  .menu-btn{display:block}
  .foot{grid-template-columns:1fr 1fr;gap:28px}
  .dua-kolom{grid-template-columns:1fr}
}
@media(max-width:640px){
  .section{padding:54px 0}
  .hero-kecil{padding:42px 0 44px}
  .hero-poin{grid-template-columns:1fr}
  .foot{grid-template-columns:1fr}
  .hero-cta,.cta-tombol{flex-direction:column}
  .hero-cta .btn,.cta-tombol .btn{width:100%}
  .cta-akhir{padding:60px 0}
}
"""

# ============================================================
# CSS v3 — REDESIGN PREMIUM (anti-aliased, glass, gradient, motion)
# Lapisan ini menimpa (override) style lama, jadi aman.
# ============================================================
CSS_V3 = """
/* ============================================================
   ARTA TEKNIK v3 — Premium pass
   ============================================================ */
:root{
  --grad-hero:linear-gradient(155deg,#061a35 0%,#0b2a4e 42%,#123a63 78%,#17477a 100%);
  --glass:rgba(255,255,255,.075);
  --glass-b:rgba(255,255,255,.16);
  --shadow-soft:0 18px 48px -18px rgba(11,42,78,.28);
  --shadow-pop:0 30px 70px -22px rgba(11,42,78,.42);
  --r-xl:26px;
  --ease:cubic-bezier(.22,.75,.28,1);
}
body{background:#fbfdff}

/* ---------- Header premium ---------- */
header{background:rgba(255,255,255,.82);backdrop-filter:blur(18px) saturate(160%);
  -webkit-backdrop-filter:blur(18px) saturate(160%);border-bottom:1px solid rgba(217,232,247,.9)}
header.gulir{background:rgba(255,255,255,.94);
  box-shadow:0 10px 34px -14px rgba(11,42,78,.22)}
.brand svg{transition:transform .4s var(--ease)}
.brand:hover svg{transform:rotate(-8deg) scale(1.06)}
nav a{position:relative;padding:8px 2px}
nav a::after{content:"";position:absolute;left:0;right:100%;bottom:2px;height:2px;
  border-radius:2px;background:var(--grad-gold);transition:right .3s var(--ease)}
nav a:hover::after,nav a.aktif::after{right:0}
nav .btn::after{display:none}
.btn-gold{position:relative;overflow:hidden;border-radius:12px}
.btn-gold::before{content:"";position:absolute;inset:0;
  background:linear-gradient(120deg,transparent 25%,rgba(255,255,255,.55),transparent 75%);
  transform:translateX(-130%);transition:transform .7s var(--ease)}
.btn-gold:hover::before{transform:translateX(130%)}

/* ---------- Hero premium ---------- */
.hero{padding:96px 0 112px;background:var(--grad-hero)}
.hero::before{background:
  radial-gradient(circle at 82% 8%,rgba(46,134,222,.42),transparent 46%),
  radial-gradient(circle at 8% 92%,rgba(244,180,0,.20),transparent 42%),
  radial-gradient(circle at 55% 120%,rgba(46,134,222,.18),transparent 60%)}
.hero::after{content:"";position:absolute;left:0;right:0;bottom:-1px;height:90px;
  background:linear-gradient(to top,#fbfdff,transparent);pointer-events:none;z-index:3}
.hero-grid-lines{background-size:52px 52px;opacity:.85;
  animation:gridDrift 34s linear infinite}
@keyframes gridDrift{to{background-position:52px 52px}}
.hero h1{font-size:clamp(35px,5.4vw,58px);text-shadow:0 2px 30px rgba(0,0,0,.22)}
.hero h1 em{background:var(--grad-gold);-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent;color:var(--gold)}
.hero-badge{animation:fadeUp .7s var(--ease) both}
.hero h1{animation:fadeUp .7s .06s var(--ease) both}
.hero p.lead{animation:fadeUp .7s .12s var(--ease) both}
.hero-ctas{animation:fadeUp .7s .18s var(--ease) both}
.mini-icons{animation:fadeUp .7s .24s var(--ease) both}
@keyframes fadeUp{from{opacity:0;transform:translateY(18px)}to{opacity:1;transform:none}}
.hero-ctas .btn{position:relative}
.btn-wa{background:linear-gradient(135deg,#2ee06f,#1eb955);color:#fff!important;
  box-shadow:0 14px 32px -10px rgba(37,211,102,.6);border-radius:13px}
.btn-wa:hover{box-shadow:0 20px 42px -12px rgba(37,211,102,.7)}
.btn-ghost{background:var(--glass);border:1.5px solid var(--glass-b);border-radius:13px;
  backdrop-filter:blur(10px)}
.btn-ghost:hover{background:rgba(255,255,255,.18);border-color:rgba(255,255,255,.45)}

/* Stats bar */
.hero-stats-v3{display:flex;gap:14px;flex-wrap:wrap;margin-top:38px;
  animation:fadeUp .7s .3s var(--ease) both}
.hsv{flex:1 1 130px;background:var(--glass);border:1px solid var(--glass-b);
  border-radius:16px;padding:15px 18px;backdrop-filter:blur(10px);text-align:left;
  transition:transform .3s var(--ease),background .3s,box-shadow .3s}
.hsv:hover{transform:translateY(-5px);background:rgba(255,255,255,.13);
  box-shadow:0 16px 34px -14px rgba(0,0,0,.4)}
.hsv b{display:block;font-family:"Sora",sans-serif;font-size:24px;font-weight:800;
  color:var(--gold);line-height:1}
.hsv span{font-size:12px;color:rgba(255,255,255,.72);font-weight:600;
  letter-spacing:.2px;display:block;margin-top:5px}

/* Visual scene (panel kanan hero) */
.scene-wrap{position:relative;animation:fadeUp .8s .15s var(--ease) both}
.scene-card{background:linear-gradient(160deg,rgba(255,255,255,.13),rgba(255,255,255,.045));
  border:1px solid var(--glass-b);border-radius:var(--r-xl);padding:16px;
  backdrop-filter:blur(16px);box-shadow:var(--shadow-pop);position:relative;overflow:hidden}
.scene-card::before{content:"";position:absolute;top:-60%;left:-30%;width:70%;height:220%;
  background:linear-gradient(100deg,transparent,rgba(255,255,255,.14),transparent);
  transform:rotate(18deg);animation:sheen 7s ease-in-out infinite}
@keyframes sheen{0%,70%{transform:translateX(-40%) rotate(18deg)}100%{transform:translateX(340%) rotate(18deg)}}
.tabs-v3{display:grid;grid-template-columns:1fr 1fr;gap:6px;background:rgba(0,0,0,.3);
  border-radius:14px;padding:5px;margin-bottom:14px;position:relative;z-index:2}
.tabs-v3 button{background:none;border:0;color:#bcd6f2;font:700 14.5px "Plus Jakarta Sans",sans-serif;
  padding:11px;border-radius:10px;cursor:pointer;transition:all .28s var(--ease)}
.tabs-v3 button[aria-selected="true"]{background:var(--grad-gold);color:var(--navy);
  box-shadow:0 8px 20px -8px rgba(244,180,0,.75)}
.scene{display:none}
.scene.on{display:block;animation:fadeUp .45s var(--ease) both}
.scene svg{width:100%;height:auto;border-radius:16px;display:block}
.scene-cap{display:flex;justify-content:space-between;align-items:center;gap:12px;
  padding:14px 16px;margin-top:12px;background:rgba(0,0,0,.28);border-radius:14px;
  font-size:13.5px;color:rgba(255,255,255,.85);position:relative;z-index:2}
.scene-cap b{color:var(--gold);font-family:"Sora",sans-serif;font-size:15px}
.scene-cap .live{display:inline-flex;align-items:center;gap:7px}
.scene-cap .live i{width:7px;height:7px;border-radius:50%;background:#3ddc84;
  animation:pulseDot 1.7s infinite}
@keyframes pulseDot{0%{box-shadow:0 0 0 0 rgba(61,220,132,.65)}70%{box-shadow:0 0 0 8px rgba(61,220,132,0)}100%{box-shadow:0 0 0 0 rgba(61,220,132,0)}}
/* animasi dalam SVG */
.wv{fill:none;stroke:#7fd4ff;stroke-width:3.4;stroke-linecap:round;opacity:.5;
  animation:wv 2.6s ease-in-out infinite}
.wv:nth-of-type(2){animation-delay:.35s}.wv:nth-of-type(3){animation-delay:.7s}
@keyframes wv{0%,100%{transform:translateY(0);opacity:.22}50%{transform:translateY(15px);opacity:.75}}
.flk{fill:#d8f1ff;animation:flk 4.2s linear infinite}
.flk:nth-of-type(2){animation-delay:-1.1s;animation-duration:5.1s}
.flk:nth-of-type(3){animation-delay:-2.2s}
.flk:nth-of-type(4){animation-delay:-3.1s;animation-duration:4.6s}
.flk:nth-of-type(5){animation-delay:-.6s;animation-duration:5.6s}
.flk:nth-of-type(6){animation-delay:-2.7s}
@keyframes flk{0%{transform:translateY(-8px);opacity:0}12%{opacity:1}100%{transform:translateY(155px);opacity:0}}
.sweep{transform-origin:158px 92px;animation:sweep 4.4s ease-in-out infinite;fill:url(#bmGrad)}
@keyframes sweep{0%,100%{transform:rotate(-15deg)}50%{transform:rotate(17deg)}}
.recDot{fill:#ff4d4d;animation:blink 1.25s steps(2,start) infinite}
@keyframes blink{50%{opacity:0}}

/* ---------- Trust marquee ---------- */
.trust-bar{background:#fff;border-bottom:1px solid var(--sky-border);padding:18px 0;
  overflow:hidden;position:relative}
.trust-bar::before,.trust-bar::after{content:"";position:absolute;top:0;bottom:0;width:80px;
  z-index:2;pointer-events:none}
.trust-bar::before{left:0;background:linear-gradient(to right,#fff,transparent)}
.trust-bar::after{right:0;background:linear-gradient(to left,#fff,transparent)}
.trust-track{display:flex;gap:44px;white-space:nowrap;will-change:transform;
  animation:marquee 34s linear infinite;width:max-content}
.trust-track:hover{animation-play-state:paused}
@keyframes marquee{to{transform:translateX(-50%)}}
.trust-track span{display:inline-flex;align-items:center;gap:9px;font-size:14px;
  font-weight:600;color:var(--muted)}
.trust-track b{color:var(--navy);font-weight:800}
.trust-track svg{color:var(--gold);flex:none}

/* ---------- Section polish ---------- */
.section-title .kicker{display:inline-block;font-size:12px;font-weight:800;
  letter-spacing:2.2px;text-transform:uppercase;color:var(--blue);
  background:rgba(28,95,176,.09);padding:6px 14px;border-radius:100px;margin-bottom:16px}
.section h2{letter-spacing:-.9px}
.section-title{text-align:center;max-width:720px;margin:0 auto 48px}
.section-title p{margin-top:2px}
.section-title h2{margin-bottom:12px}
.kartu-l,.area-kartu,.info-item,.faq-item{box-shadow:var(--shadow-soft)}
.kartu-l{position:relative;overflow:hidden}
.kartu-l::before{content:"";position:absolute;inset:0 0 auto 0;height:4px;
  background:var(--grad-gold);transform:scaleX(0);transform-origin:left;
  transition:transform .4s var(--ease)}
.kartu-l:hover::before{transform:scaleX(1)}
.kartu-l .ikon{transition:transform .35s var(--ease),background .3s}
.kartu-l:hover .ikon{transform:translateY(-3px) scale(1.06)}
.kartu-l:hover h3{color:var(--blue)}
.kartu-l h3{transition:color .3s}
.area-kartu{position:relative;overflow:hidden}
.area-kartu::after{content:"";position:absolute;right:-40px;bottom:-40px;width:130px;height:130px;
  border-radius:50%;background:radial-gradient(circle,rgba(28,95,176,.10),transparent 70%);
  transition:transform .5s var(--ease)}
.area-kartu:hover::after{transform:scale(1.6)}
.keunggulan-ikon{box-shadow:0 10px 26px -12px rgba(11,42,78,.35)}
.faq-item[open]{transform:translateY(-2px)}
.kotak-rating{border:1px solid var(--sky-border);position:relative;overflow:hidden;
  background:linear-gradient(150deg,#fff,#f7fbff);box-shadow:var(--shadow-soft)}
.kotak-rating::before{content:"";position:absolute;right:-70px;top:-70px;width:200px;height:200px;
  border-radius:50%;background:radial-gradient(circle,rgba(244,180,0,.12),transparent 68%)}
.rating-angka{background:var(--grad-navy);-webkit-background-clip:text;background-clip:text;
  -webkit-text-fill-color:transparent}

/* ---------- CTA akhir ---------- */
.cta-akhir{background:var(--grad-hero);padding:88px 0}
.cta-akhir::after{width:620px;height:620px}
.cta-akhir h2{letter-spacing:-1px}
.cta-tombol{animation:none}

/* ---------- Footer ---------- */
footer{background:linear-gradient(180deg,#0a1f3a,#061a30);position:relative;overflow:hidden}
footer::before{content:"";position:absolute;left:-120px;top:-140px;width:420px;height:420px;
  border-radius:50%;background:radial-gradient(circle,rgba(28,95,176,.16),transparent 70%)}

/* ---------- WhatsApp FAB ---------- */
.fab{position:fixed;right:18px;bottom:18px;z-index:120;display:inline-flex;align-items:center;
  gap:11px;background:linear-gradient(135deg,#2ee06f,#1eb955);color:#fff;font-weight:800;
  font-size:14.5px;padding:0 22px 0 17px;height:58px;border-radius:100px;text-decoration:none;
  box-shadow:0 16px 38px -12px rgba(37,211,102,.7);
  transform:translateY(110px) scale(.85);opacity:0;
  transition:transform .45s var(--ease),opacity .35s,box-shadow .3s}
.fab.show{transform:none;opacity:1}
.fab:hover{box-shadow:0 22px 48px -14px rgba(37,211,102,.85);transform:translateY(-3px)}
.fab svg{width:27px;height:27px;flex:none}
.fab::after{content:"";position:absolute;inset:0;border-radius:100px;
  border:2px solid rgba(37,211,102,.5);animation:ring 2.4s ease-out infinite}
@keyframes ring{0%{transform:scale(1);opacity:.7}100%{transform:scale(1.22);opacity:0}}
@media(max-width:520px){.fab span{display:none}.fab{width:58px;padding:0;justify-content:center}}

/* ---------- Scroll reveal ---------- */
.reveal{opacity:0;transform:translateY(30px);transition:opacity .75s var(--ease),transform .75s var(--ease)}
.reveal.visible{opacity:1;transform:none}
.reveal.d1{transition-delay:.08s}.reveal.d2{transition-delay:.16s}
.reveal.d3{transition-delay:.24s}.reveal.d4{transition-delay:.32s}

/* ---------- Responsif v3 ---------- */
@media(max-width:980px){
  .hero{padding:72px 0 86px}
  .hero-inner{gap:38px}
  .scene-wrap{order:-1}
}
@media(max-width:640px){
  .hero{padding:56px 0 68px}
  .hero-stats-v3{gap:10px}
  .hsv{flex:1 1 44%;padding:13px 15px}
  .hsv b{font-size:21px}
  .cta-akhir{padding:64px 0}
}
@media(prefers-reduced-motion:reduce){
  *,*::before,*::after{animation:none!important;transition:none!important}
  .reveal{opacity:1;transform:none}
  .fab{transform:none;opacity:1}
}
"""

# ============================================================
# TEMPLATE KOMPONEN
# ============================================================
def fab_wa():
    """Tombol WhatsApp melayang (muncul setelah scroll)."""
    link = wa_pesan(f"Assalamualaikum {B['nama']}, saya butuh bantuan.")
    return f"""<a class="fab" id="fabWa" href="{link}" target="_blank" rel="noopener" aria-label="Chat WhatsApp {esc(B['nama'])}">
  <svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 2a8 8 0 016.9 12l-.4.6 1 3.5-3.6-1-.6.4A8 8 0 1112 4zm-3.3 4c-.2 0-.5.1-.7.4-.3.3-.9 1-.9 2s.7 2.1.8 2.2c.1.2 1.4 2.2 3.4 3 1.7.7 2 .6 2.4.5.4 0 1.2-.4 1.4-1 .2-.5.2-1 .1-1.1 0-.1-.2-.2-.4-.3l-1.4-.7c-.2-.1-.4-.1-.5.1l-.6.8c-.1.2-.3.2-.5.1-.2-.1-.9-.4-1.7-1.1-.6-.6-1-1.2-1.1-1.4-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5 0-.2 0-.3-.1-.4l-.6-1.5c-.2-.4-.3-.4-.5-.4z"/></svg>
  <span>Chat WhatsApp</span>
</a>"""


def blok_trust():
    """Pita berjalan (marquee) berisi kepercayaan — dipakai di beranda."""
    ikon_c = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5 9.5 18 20 6"/></svg>'
    ikon_s = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M12 2l2.9 6.3 6.9.9-5 4.8 1.3 6.8L12 17.6 5.9 20.8 7.2 14l-5-4.8 6.9-.9z"/></svg>'
    item = [
        ("Rating", f"{B['rating']} di Google"),
        ("Garansi", "setiap pekerjaan"),
        ("Layanan", "panggilan ke lokasi"),
        ("Area", "Solo, Sukoharjo, Karanganyar"),
        ("Bayar", "setelah cek hasil"),
        ("Teknisi", "berpengalaman &amp; rapi"),
        ("Jadwal", "Senin - Sabtu, 08.00 - 20.00 WIB"),
    ]
    satu = ""
    for k, v in item:
        ico = ikon_s if k == "Rating" else ikon_c
        satu += f"        <span>{ico}<b>{esc(k)}</b> {v}</span>\n"
    # duplikat supaya loop mulus
    return ("""<div class="trust-bar" aria-hidden="true">
  <div class="trust-track">
""" + satu + satu + """  </div>
</div>""")


def header(aktif=""):
    menu = [
        ("Beranda", "index.html"),
        ("Servis AC", "layanan/servis-ac.html"),
        ("Pasang AC", "layanan/pasang-ac.html"),
        ("CCTV", "layanan/pasang-cctv.html"),
        ("Area", "area/solo.html"),
        ("Kontak", "kontak.html"),
    ]
    item = ""
    for label, link in menu:
        cls = ' class="aktif"' if label == aktif else ""
        item += f'<a href="{{{{REL}}}}{link}"{cls}>{esc(label)}</a>\n      '
    return f"""<header id="header">
  <div class="container bar">
    <a class="brand" href="{_rel('index.html')}">
      <svg viewBox="0 0 48 48" width="40" height="40" role="img" aria-label="Logo {esc(B['nama'])}">
        <rect x="4" y="4" width="40" height="40" rx="11" fill="#0b2a4e"/>
        <path d="M24 13l11 6v11l-11 6-11-6V19z" fill="none" stroke="#f4b400" stroke-width="2.2" stroke-linejoin="round"/>
        <circle cx="24" cy="24" r="4" fill="#f4b400"/>
      </svg>
      <span>
        <span class="nm-brand">{esc(B['nama'])}</span>
        <span class="sub-brand">{esc(B['tagline'])}</span>
      </span>
    </a>
    <button class="menu-btn" id="menuBtn" aria-expanded="false" aria-controls="navUtama" aria-label="Buka menu">&#9776;</button>
    <nav id="navUtama" aria-label="Navigasi utama">
      {item}<a class="btn btn-gold" href="{_rel('kontak.html')}">Hubungi Kami</a>
    </nav>
  </div>
</header>"""


def footer():
    return f"""<footer>
  <div class="container">
    <div class="foot">
      <div>
        <div class="brand-foot">
          <svg viewBox="0 0 48 48" width="38" height="38" role="img" aria-label="Logo {esc(B['nama'])}">
            <rect x="4" y="4" width="40" height="40" rx="11" fill="#10345f"/>
            <path d="M24 13l11 6v11l-11 6-11-6V19z" fill="none" stroke="#f4b400" stroke-width="2.2" stroke-linejoin="round"/>
            <circle cx="24" cy="24" r="4" fill="#f4b400"/>
          </svg>
          <span class="nm-foot">{esc(B['nama'])}</span>
        </div>
        <p>{esc(B['deskripsi'])} di Solo, Sukoharjo, dan Karanganyar.</p>
      </div>
      <div>
        <h4>Layanan</h4>
        <ul>
          <li><a href="{_rel('layanan/servis-ac.html')}">Servis AC</a></li>
          <li><a href="{_rel('layanan/pasang-ac.html')}">Pasang AC</a></li>
          <li><a href="{_rel('layanan/pasang-cctv.html')}">Pasang CCTV</a></li>
        </ul>
      </div>
      <div>
        <h4>Area Layanan</h4>
        <ul>
          <li><a href="{_rel('area/solo.html')}">Solo (Surakarta)</a></li>
          <li><a href="{_rel('area/sukoharjo.html')}">Sukoharjo</a></li>
          <li><a href="{_rel('area/karanganyar.html')}">Karanganyar</a></li>
        </ul>
      </div>
      <div>
        <h4>Kontak</h4>
        <ul>
          <li><a href="tel:+{esc(WA)}">{esc(B['telepon_display'])}</a></li>
          <li><a href="{wa_pesan(f"Assalamualaikum {B['nama']}, saya ingin konsultasi.")}" target="_blank" rel="noopener">WhatsApp</a></li>
          <li>{esc(B['jam_kerja'])}</li>
        </ul>
      </div>
    </div>
    <div class="foot-bottom">
      <span>&copy; {date.today().year} {esc(B['nama'])}. Seluruh hak cipta dilindungi.</span>
      <span>{esc(B['tagline'])} &middot; Solo Raya</span>
    </div>
  </div>
</footer>"""


def skrip():
    return """<script>
(function(){
  var h = document.getElementById('header');
  if(h){
    function cek(){ h.classList.toggle('gulir', window.scrollY > 30); }
    cek(); window.addEventListener('scroll', cek, {passive:true});
  }
  var btn = document.getElementById('menuBtn');
  var nav = document.getElementById('navUtama');
  if(!btn || !nav) return;
  function tutup(){ nav.classList.remove('open'); btn.setAttribute('aria-expanded','false'); btn.innerHTML='&#9776;'; }
  function buka(){ nav.classList.add('open'); btn.setAttribute('aria-expanded','true'); btn.innerHTML='&times;'; }
  btn.addEventListener('click', function(){ nav.classList.contains('open') ? tutup() : buka(); });
  nav.querySelectorAll('a').forEach(function(a){ a.addEventListener('click', tutup); });
  document.addEventListener('keydown', function(e){
    if(e.key === 'Escape' && nav.classList.contains('open')){ tutup(); btn.focus(); }
  });
  window.addEventListener('resize', function(){ if(window.innerWidth > 900) tutup(); });

  /* --- Tab hero v3 (Servis AC / Pasang CCTV) --- */
  var pasang = [['tAC','sAC'],['tCCTV','sCCTV']];
  pasang.forEach(function(p){
    var tombol = document.getElementById(p[0]);
    if(!tombol) return;
    tombol.addEventListener('click', function(){
      pasang.forEach(function(q){
        var aktif = (q[0] === p[0]);
        document.getElementById(q[0]).setAttribute('aria-selected', aktif);
        document.getElementById(q[1]).classList.toggle('on', aktif);
      });
    });
  });

  /* --- Scroll reveal --- */
  var els = document.querySelectorAll('.reveal');
  if('IntersectionObserver' in window){
    var io = new IntersectionObserver(function(entries){
      entries.forEach(function(e){
        if(e.isIntersecting){ e.target.classList.add('visible'); io.unobserve(e.target); }
      });
    }, {threshold:0.12, rootMargin:'0px 0px -40px 0px'});
    els.forEach(function(e){ io.observe(e); });
  } else {
    els.forEach(function(e){ e.classList.add('visible'); });
  }

  /* --- Tombol WhatsApp melayang --- */
  var fab = document.getElementById('fabWa');
  if(fab){
    function cekFab(){ fab.classList.toggle('show', window.scrollY > 380); }
    cekFab(); window.addEventListener('scroll', cekFab, {passive:true});
  }
})();
</script>"""


# Kedalaman folder (untuk link relatif)
KEDALAMAN = {"": 0, "layanan": 1, "area": 1}

def _rel(tujuan):
    """Bikin link relatif dari halaman saat ini."""
    return "{{REL}}" + tujuan


def halaman(judul, deskripsi, isi, aktif="", kedalaman=0, canonical="",
            schema_extra="", og_gambar="og-cover.png"):
    """Bikin satu halaman HTML lengkap."""
    pref = "../" * kedalaman
    rel = "" if kedalaman == 0 else "../" * kedalaman

    # Ganti placeholder REL
    isi_final = isi.replace("{{REL}}", rel)
    head_final = header(aktif).replace("{{REL}}", rel)
    foot_final = footer().replace("{{REL}}", rel)

    canon = f"{DOMAIN}/{canonical}" if canonical else f"{DOMAIN}/"

    verif_gsc = (f'<meta name="google-site-verification" content="{GSC_VERIFIKASI}">'
                 if GSC_VERIFIKASI else "")

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(judul)}</title>
<meta name="description" content="{esc(deskripsi)}">
<meta name="robots" content="index, follow, max-image-preview:large, max-snippet:-1, max-video-preview:-1">
<link rel="canonical" href="{canon}">
{verif_gsc}
<!-- Geo / SEO lokal (bantu Google & AI paham wilayah layanan) -->
<meta name="geo.region" content="ID-JT">
<meta name="geo.placename" content="{esc(B['alamat']['kota'])}, Jawa Tengah">
<meta name="geo.position" content="-7.5890876;110.977259">
<meta name="ICBM" content="-7.5890876, 110.977259">
<meta name="language" content="Indonesian">
<meta name="author" content="{esc(B['nama'])}">
<meta name="theme-color" content="#0b2a4e">

<!-- Favicon (inline SVG, tidak butuh file tambahan) -->
<link rel="icon" type="image/svg+xml" href="{pref}favicon.svg">
<link rel="apple-touch-icon" href="{pref}favicon.svg">
<link rel="manifest" href="{pref}site.webmanifest">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(B['nama'])}">
<meta property="og:title" content="{esc(judul)}">
<meta property="og:description" content="{esc(deskripsi)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/{og_gambar}">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:image:alt" content="{esc(B['nama_resmi'])}">
<meta property="og:locale" content="id_ID">
<meta property="business:contact_data:street_address" content="Melayani panggilan (Solo Raya)">
<meta property="business:contact_data:locality" content="{esc(B['alamat']['kota'])}">
<meta property="business:contact_data:region" content="{esc(B['alamat']['region'])}">
<meta property="business:contact_data:country_name" content="Indonesia">
<meta property="business:contact_data:phone_number" content="+{esc(WA)}">
<meta property="business:contact_data:website" content="{DOMAIN}/">

<!-- Twitter -->
<meta name="twitter:card" content="summary_large_image">
<meta name="twitter:title" content="{esc(judul)}">
<meta name="twitter:description" content="{esc(deskripsi)}">
<meta name="twitter:image" content="{DOMAIN}/{og_gambar}">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
<style>
{CSS}
{CSS_TAMBAHAN}
{CSS_V3}
</style>
{schema_extra}
</head>
<body>
{head_final}
{isi_final}
{foot_final}
{fab_wa()}
{skrip()}
</body>
</html>"""


# ============================================================
# SCHEMA JSON-LD
# ============================================================
def schema_bisnis():
    area = ", ".join([f"{a['nama']}" for a in DATA["area"]])
    # areaServed rinci: kota + kecamatan (bantu AI paham cakupan lokal)
    served = []
    for a in DATA["area"]:
        served.append(f'    {{\n      "@type": "City",\n      "name": "{esc(a["nama_lengkap"])}",'
                      f'\n      "containedInPlace": {{"@type": "AdministrativeArea", "name": "Jawa Tengah"}}'
                      f'\n    }}')
        for k in a["kecamatan"]:
            served.append(f'    {{\n      "@type": "AdministrativeArea",\n      '
                          f'"name": "Kecamatan {esc(k)}, {esc(a["nama_lengkap"])}"\n    }}')
    area_served = ",\n".join(served)

    return f"""{{
  "@context": "https://schema.org",
  "@type": ["HVACBusiness", "LocalBusiness", "HomeAndConstructionBusiness"],
  "@id": "{DOMAIN}/#bisnis",
  "name": "{esc(B['nama'])}",
  "alternateName": "{esc(B['nama_resmi'])}",
  "description": "Jasa servis AC, pasang AC, dan pasang CCTV panggilan (teknisi datang ke lokasi) di {esc(area)}. Bergaransi.",
  "url": "{DOMAIN}/",
  "telephone": "+{esc(WA)}",
  "email": "{esc(B['email'])}",
  "priceRange": "Rp",
  "currenciesAccepted": "IDR",
  "paymentAccepted": "Tunai, Transfer Bank, QRIS",
  "image": [
    "{DOMAIN}/og-cover.png"
  ],
  "logo": "{DOMAIN}/favicon.svg",
  "address": {{
    "@type": "PostalAddress",
    "addressLocality": "{esc(B['alamat']['kota'])}",
    "addressRegion": "{esc(B['alamat']['region'])}",
    "addressCountry": "{esc(B['alamat']['negara'])}"
  }},
  "areaServed": [
{area_served}
  ],
  "serviceArea": {{
    "@type": "GeoCircle",
    "geoMidpoint": {{
      "@type": "GeoCoordinates",
      "latitude": -7.5890876,
      "longitude": 110.977259
    }},
    "geoRadius": "35000"
  }},
  "knowsAbout": [
    "Servis AC", "Cuci AC", "Isi Freon AC", "Bongkar Pasang AC",
    "Pemasangan AC Baru", "Perbaikan AC Tidak Dingin", "Perbaikan AC Bocor",
    "Pemasangan CCTV", "Setting DVR NVR", "Monitoring CCTV dari HP",
    "Perbaikan CCTV", "Penambahan Kamera CCTV"
  ],
  "slogan": "{esc(B['tagline'])}",
  "foundingDate": "{B['tahun_mulai']}",
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "{B['rating']}",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "{DATA['bisnis'].get('jumlah_ulasan') or 27}"
  }},
  "sameAs": [
    "{B['google_maps']}"
  ],
  "hasMap": "{B['google_maps']}",
  "openingHoursSpecification": {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "opens": "08:00",
    "closes": "20:00"
  }},
  "availableChannel": {{
    "@type": "ServiceChannel",
    "servicePhone": {{
      "@type": "ContactPoint",
      "telephone": "+{esc(WA)}",
      "contactType": "customer service",
      "availableLanguage": ["id"]
    }},
    "serviceUrl": "https://wa.me/{esc(WA)}"
  }},
  "makesOffer": [
{', '.join([f'''    {{
      "@type": "Offer",
      "itemOffered": {{"@type": "Service", "name": "{esc(l['nama'])}", "url": "{DOMAIN}/layanan/{l['slug']}.html"}}
    }}''' for l in DATA["layanan"]])}
  ],
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Layanan {esc(B['nama'])}",
    "itemListElement": [
{', '.join([f'''      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "{esc(l['nama'])}", "url": "{DOMAIN}/layanan/{l['slug']}.html"}}}}''' for l in DATA["layanan"]])}
    ]
  }}
}}"""


def schema_kontak():
    """ContactPage -> bantu AI tahu halaman ini untuk menghubungi bisnis."""
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "ContactPage",
  "@id": "{DOMAIN}/kontak.html#kontak",
  "url": "{DOMAIN}/kontak.html",
  "name": "Hubungi {esc(B['nama'])}",
  "inLanguage": "id-ID",
  "about": {{"@id": "{DOMAIN}/#bisnis"}},
  "mainEntity": {{
    "@type": "Organization",
    "name": "{esc(B['nama'])}",
    "telephone": "+{esc(WA)}",
    "email": "{esc(B['email'])}",
    "contactPoint": {{
      "@type": "ContactPoint",
      "telephone": "+{esc(WA)}",
      "contactType": "customer service",
      "areaServed": "ID",
      "availableLanguage": ["id"]
    }}
  }}
}}
</script>"""


def schema_website():
    """WebSite + SearchAction -> bantu AI & Google paham situs ini apa."""
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "@id": "{DOMAIN}/#website",
  "url": "{DOMAIN}/",
  "name": "{esc(B['nama'])}",
  "alternateName": "{esc(B['nama_resmi'])}",
  "description": "{esc(B['deskripsi'])} di Solo, Sukoharjo, dan Karanganyar.",
  "inLanguage": "id-ID",
  "publisher": {{"@id": "{DOMAIN}/#bisnis"}}
}}
</script>"""


def schema_area(a):
    """Service + Place khusus halaman area, biar kuat untuk pencarian lokal."""
    served = [f'    {{"@type": "AdministrativeArea", "name": "Kecamatan {esc(k)}, {esc(a["nama_lengkap"])}"}}'
              for k in a["kecamatan"]]
    area_json = ",\n".join(served)
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "{DOMAIN}/area/{a['slug']}.html#layanan",
  "name": "Servis AC & Pasang CCTV di {esc(a['nama'])}",
  "serviceType": "Servis AC, Pasang AC, Pasang CCTV",
  "provider": {{"@id": "{DOMAIN}/#bisnis"}},
  "description": "{esc(a['catatan'])}",
  "url": "{DOMAIN}/area/{a['slug']}.html",
  "areaServed": [
{area_json}
  ],
  "availableChannel": {{
    "@type": "ServiceChannel",
    "serviceUrl": "https://wa.me/{esc(WA)}",
    "servicePhone": {{"@type": "ContactPoint", "telephone": "+{esc(WA)}"}}
  }}
}}
</script>"""


def schema_breadcrumb(jejak):
    """jejak = list of (nama, url_relatif). Bantu Google tampilkan breadcrumb."""
    items = []
    for i, (nama, url) in enumerate(jejak, 1):
        rapi = f"{DOMAIN}/{url}" if url else f"{DOMAIN}/"
        items.append(f'''    {{
      "@type": "ListItem",
      "position": {i},
      "name": "{esc(nama)}",
      "item": "{rapi}"
    }}''')
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
{', '.join(items)}
  ]
}}
</script>"""


def schema_faq(daftar):
    if not daftar: return ""
    items = ",\n".join([f'''    {{
      "@type": "Question",
      "name": "{esc(x['q'])}",
      "acceptedAnswer": {{"@type": "Answer", "text": "{esc(x['a'])}"}}
    }}''' for x in daftar])
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "FAQPage",
  "mainEntity": [
{items}
  ]
}}
</script>"""


def schema_layanan(l):
    # areaServed rinci sampai kecamatan -> bantu GEO
    served = []
    for a in DATA["area"]:
        served.append(f'    {{"@type": "City", "name": "{esc(a["nama_lengkap"])}"}}')
        for k in a["kecamatan"]:
            served.append(f'    {{"@type": "AdministrativeArea", "name": "Kecamatan {esc(k)}"}}')
    area_json = ",\n".join(served)
    layanan_lain = [x for x in DATA["layanan"] if x["slug"] != l["slug"]]
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "@id": "{DOMAIN}/layanan/{l['slug']}.html#layanan",
  "name": "{esc(l['judul_seo'])}",
  "serviceType": "{esc(l['nama'])}",
  "provider": {{"@id": "{DOMAIN}/#bisnis"}},
  "areaServed": [
{area_json}
  ],
  "aggregateRating": {{
    "@type": "AggregateRating",
    "ratingValue": "{B['rating']}",
    "bestRating": "5",
    "worstRating": "1",
    "ratingCount": "{DATA['bisnis'].get('jumlah_ulasan') or 27}"
  }},
  "sameAs": [
    "{B['google_maps']}"
  ],
  "description": "{esc(l['deskripsi_seo'])}",
  "url": "{DOMAIN}/layanan/{l['slug']}.html",
  "category": "Jasa Teknik AC & CCTV",
  "availableChannel": {{
    "@type": "ServiceChannel",
    "serviceUrl": "https://wa.me/{esc(WA)}",
    "servicePhone": {{"@type": "ContactPoint", "telephone": "+{esc(WA)}"}}
  }},
  "isRelatedTo": [
{', '.join([f'    {{"@type": "Service", "name": "{esc(x["nama"])}", "url": "{DOMAIN}/layanan/{x["slug"]}.html"}}' for x in layanan_lain])}
  ]
}}
</script>"""


def schema_breadcrumb(jejak):
    """jejak = [(nama, url), ...]"""
    items = ",\n".join([f'''    {{
      "@type": "ListItem",
      "position": {i+1},
      "name": "{esc(n)}",
      "item": "{DOMAIN}/{u}"
    }}''' for i, (n, u) in enumerate(jejak)])
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "BreadcrumbList",
  "itemListElement": [
{items}
  ]
}}
</script>"""


# ============================================================
# BLOK BERSAMA
# ============================================================
def blok_keunggulan():
    kartu = ""
    kelas_huruf = ["", "d1", "d2", "d3"]
    for i, k in enumerate(DATA["keunggulan"]):
        kartu += f"""      <div class="keunggulan-item reveal {kelas_huruf[i % 4]}">
        <div class="keunggulan-ikon">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="#f4b400" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 12.5 9.5 18 20 6"/></svg>
        </div>
        <h3>{esc(k['judul'])}</h3>
        <p>{esc(k['teks'])}</p>
      </div>
"""
    return f"""<section class="section" id="keunggulan">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Kenapa Pilih Kami</span>
      <h2>Kenapa Pilih {esc(B['nama'])}?</h2>
      <p>Kami bekerja rapi, jujur soal harga, dan bertanggung jawab atas hasilnya.</p>
    </div>
    <div class="grid-keunggulan">
{kartu}    </div>
  </div>
</section>"""


def blok_faq(daftar, judul="Pertanyaan yang Sering Diajukan"):
    item = ""
    for i, f in enumerate(daftar):
        buka = " open" if i == 0 else ""
        item += f"""      <details class="faq-item"{buka}>
        <summary>{esc(f['q'])}</summary>
        <p>{esc(f['a'])}</p>
      </details>
"""
    return f"""<section class="section section-abu" id="faq">
  <div class="container">
    <div class="section-title">
      <span class="kicker">FAQ</span>
      <h2>{esc(judul)}</h2>
    </div>
    <div class="faq-list">
{item}    </div>
  </div>
</section>"""


def blok_cta(judul=None, teks=None):
    judul = judul or f"Butuh bantuan AC atau CCTV hari ini?"
    teks = teks or f"Hubungi {B['nama']} sekarang. Kami siap datang ke lokasi Anda di Solo, Sukoharjo, atau Karanganyar."
    return f"""<section class="seksi cta-akhir">
  <div class="container">
    <h2>{esc(judul)}</h2>
    <p>{esc(teks)}</p>
    <div class="cta-tombol">
      <a class="btn btn-wa" href="{wa_pesan(f"Assalamualaikum {B['nama']}, saya butuh bantuan.")}" target="_blank" rel="noopener">
        <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 2a8 8 0 016.9 12l-.4.6 1 3.5-3.6-1-.6.4A8 8 0 1112 4zm-3.3 4c-.2 0-.5.1-.7.4-.3.3-.9 1-.9 2s.7 2.1.8 2.2c.1.2 1.4 2.2 3.4 3 1.7.7 2 .6 2.4.5.4 0 1.2-.4 1.4-1 .2-.5.2-1 .1-1.1 0-.1-.2-.2-.4-.3l-1.4-.7c-.2-.1-.4-.1-.5.1l-.6.8c-.1.2-.3.2-.5.1-.2-.1-.9-.4-1.7-1.1-.6-.6-1-1.2-1.1-1.4-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5 0-.2 0-.3-.1-.4l-.6-1.5c-.2-.4-.3-.4-.5-.4z"/></svg>
        Chat WhatsApp
      </a>
      <a class="btn btn-outline" href="tel:+{esc(WA)}">Telepon {esc(B['telepon_display'])}</a>
    </div>
  </div>
</section>"""


def blok_kartu_layanan():
    kartu = ""
    kelas_huruf = ["", "d1", "d2"]
    for i, l in enumerate(DATA["layanan"]):
        kartu += f"""      <article class="kartu-l reveal {kelas_huruf[i % 3]}">
        <div class="ikon">
          <svg width="26" height="26" viewBox="0 0 24 24" fill="none" stroke="#1c5fb0" stroke-width="1.9" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 6h16v10H4z"/><path d="M7 10h4M7 13h2"/><circle cx="17" cy="11" r="1.6"/></svg>
        </div>
        <h3>{esc(l['nama'])}</h3>
        <p>{esc(l['deskripsi_seo'][:110])}...</p>
        <a class="tautan" href="{_rel('layanan/' + l['slug'] + '.html')}">
          Lihat detail
          <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </article>
"""
    return f"""<section class="section" id="layanan">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Layanan</span>
      <h2>Solusi AC &amp; CCTV Lengkap</h2>
      <p>Dari servis rutin sampai pemasangan baru. Semua dikerjakan teknisi berpengalaman.</p>
    </div>
    <div class="kartu-layanan">
{kartu}    </div>
  </div>
</section>"""


def blok_kartu_area():
    kartu = ""
    kelas_huruf = ["", "d1", "d2"]
    for i, a in enumerate(DATA["area"]):
        kec = ", ".join(a["kecamatan"][:6])
        sisa = len(a["kecamatan"]) - 6
        if sisa > 0:
            kec += f", dan {sisa} kecamatan lain"
        kartu += f"""      <article class="area-kartu reveal {kelas_huruf[i % 3]}">
        <h3>{esc(a['nama'])}</h3>
        <p>{esc(a['catatan'])}</p>
        <div class="kec">{esc(kec)}</div>
        <a class="tautan" href="{_rel('area/' + a['slug'] + '.html')}">
          Lihat layanan di {esc(a['nama'])}
          <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </article>
"""
    return f"""<section class="section section-abu" id="area">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Area Layanan</span>
      <h2>Melayani Solo Raya</h2>
      <p>Kami datang ke lokasi Anda. Pilih area untuk melihat cakupan lengkapnya.</p>
    </div>
    <div class="area-grid">
{kartu}    </div>
  </div>
</section>"""


# ============================================================
# HALAMAN: BERANDA
# ============================================================
def blok_rating():
    """Blok rating Google + tombol lihat ulasan."""
    return f"""
<section class="section">
  <div class="container">
    <div class="kotak-rating">
      <div class="rating-kiri">
        <div class="rating-angka">{B['rating']}</div>
        <div class="rating-bintang" aria-label="Rating {B['rating']} dari 5">★★★★★</div>
        <div class="rating-label">Rating Google</div>
      </div>
      <div class="rating-kanan">
        <h2 class="rating-judul">Dipercaya pelanggan di Solo Raya</h2>
        <p class="rating-teks">Pelanggan menilai layanan ARTA TEKNIK {B['rating']} dari 5 di Google. Penilaian ini datang dari pelanggan yang sudah memakai jasa servis dan pemasangan AC maupun CCTV kami.</p>
        <a class="btn-review" href="{B['google_maps']}" target="_blank" rel="noopener">
          <svg width="17" height="17" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2l2.9 6.3 6.9.8-5.1 4.7 1.4 6.8L12 17.2 5.9 20.6l1.4-6.8L2.2 9.1l6.9-.8z"/></svg>
          Lihat semua ulasan di Google
        </a>
      </div>
    </div>
  </div>
</section>
"""


def buat_beranda():
    judul = f"{B['nama']} — Service AC & CCTV Solo Raya | Solo, Sukoharjo, Karanganyar"
    desk = f"{B['nama']}, spesialis servis dan pemasangan AC & CCTV di Solo Raya (Solo, Sukoharjo, Karanganyar). Rating {B['rating']} di Google. Teknisi datang ke lokasi, bergaransi."

    isi = f"""<section class="hero">
  <div class="hero-grid-lines"></div>
  <div class="container hero-inner">
    <div>
      <span class="hero-badge">
        <span class="dot"></span> Spesialis AC &amp; CCTV · Solo Raya
      </span>
      <h1>AC Tidak Dingin?<br>Rumah Belum <em>Aman?</em></h1>
      <p class="lead">Kami servis AC dan pasang CCTV di Solo, Sukoharjo, dan Karanganyar. Teknisi datang ke lokasi, kerja rapi, bergaransi.</p>
      <div class="hero-ctas">
        <a class="btn btn-wa" href="{wa_pesan(f"Assalamualaikum {B['nama']}, saya butuh bantuan.")}" target="_blank" rel="noopener">
          <svg width="19" height="19" viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 2a8 8 0 016.9 12l-.4.6 1 3.5-3.6-1-.6.4A8 8 0 1112 4zm-3.3 4c-.2 0-.5.1-.7.4-.3.3-.9 1-.9 2s.7 2.1.8 2.2c.1.2 1.4 2.2 3.4 3 1.7.7 2 .6 2.4.5.4 0 1.2-.4 1.4-1 .2-.5.2-1 .1-1.1 0-.1-.2-.2-.4-.3l-1.4-.7c-.2-.1-.4-.1-.5.1l-.6.8c-.1.2-.3.2-.5.1-.2-.1-.9-.4-1.7-1.1-.6-.6-1-1.2-1.1-1.4-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5 0-.2 0-.3-.1-.4l-.6-1.5c-.2-.4-.3-.4-.5-.4z"/></svg>
          Chat WhatsApp
        </a>
        <a class="btn btn-ghost" href="{_rel('layanan/servis-ac.html')}">
          Lihat Layanan
          <svg width="15" height="15" viewBox="0 0 16 16" aria-hidden="true"><path d="M3 8h9M8.5 4l4 4-4 4" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/></svg>
        </a>
      </div>
      <div class="hero-stats-v3">
        <div class="hsv"><b>{B['rating']}/5</b><span>Rating Google</span></div>
        <div class="hsv"><b>7 Hari</b><span>Garansi pekerjaan</span></div>
        <div class="hsv"><b>3 Kota</b><span>Solo · Sukoharjo · Karanganyar</span></div>
      </div>
    </div>

    <div class="scene-wrap">
      <div class="scene-card">
        <div class="tabs-v3" role="tablist" aria-label="Pilih tampilan layanan">
          <button role="tab" id="tAC" aria-selected="true" aria-controls="sAC" type="button">Servis AC</button>
          <button role="tab" id="tCCTV" aria-selected="false" aria-controls="sCCTV" type="button">Pasang CCTV</button>
        </div>

        <div class="scene on" id="sAC" role="tabpanel" aria-labelledby="tAC">
          <svg viewBox="0 0 400 260" role="img" aria-label="Ilustrasi unit AC dingin">
            <defs>
              <linearGradient id="acBody" x1="0" y1="0" x2="0" y2="1">
                <stop offset="0" stop-color="#f7fbff"/><stop offset="1" stop-color="#dbe9f9"/>
              </linearGradient>
            </defs>
            <rect x="26" y="30" width="348" height="94" rx="22" fill="url(#acBody)"/>
            <rect x="26" y="98" width="348" height="26" rx="13" fill="#c5d9f1"/>
            <rect x="48" y="106" width="304" height="7" rx="3.5" fill="#8ea5cc"/>
            <rect x="48" y="52" width="78" height="11" rx="5.5" fill="#0b2a4e"/>
            <circle cx="340" cy="58" r="6.5" fill="#3ddc84"/>
            <circle cx="340" cy="58" r="11" fill="none" stroke="#3ddc84" stroke-opacity=".35" stroke-width="2"/>
            <path class="wv" d="M66 142 q20 15 40 0 t40 0 t40 0 t40 0 t40 0 t40 0"/>
            <path class="wv" d="M66 162 q20 15 40 0 t40 0 t40 0 t40 0 t40 0 t40 0"/>
            <path class="wv" d="M66 182 q20 15 40 0 t40 0 t40 0 t40 0 t40 0 t40 0"/>
            <g>
              <circle class="flk" cx="88" cy="132" r="4"/>
              <circle class="flk" cx="146" cy="138" r="3"/>
              <circle class="flk" cx="206" cy="132" r="5"/>
              <circle class="flk" cx="258" cy="140" r="3"/>
              <circle class="flk" cx="312" cy="134" r="4"/>
              <circle class="flk" cx="178" cy="140" r="3"/>
            </g>
          </svg>
          <div class="scene-cap">
            <span class="live"><i></i> Cuci AC + check up</span>
            <b>Rp80.000</b>
          </div>
        </div>

        <div class="scene" id="sCCTV" role="tabpanel" aria-labelledby="tCCTV">
          <svg viewBox="0 0 400 260" role="img" aria-label="Ilustrasi kamera CCTV memantau">
            <defs>
              <linearGradient id="bmGrad" x1="0" y1="0" x2="1" y2="0">
                <stop offset="0" stop-color="#7fd4ff" stop-opacity=".55"/>
                <stop offset="1" stop-color="#7fd4ff" stop-opacity="0"/>
              </linearGradient>
            </defs>
            <polygon class="sweep" points="152,92 400,4 400,214"/>
            <rect x="58" y="68" width="112" height="44" rx="13" fill="#f4f8ff"/>
            <rect x="150" y="75" width="36" height="31" rx="9" fill="#0b2a4e" stroke="#f4f8ff" stroke-width="3"/>
            <circle cx="168" cy="90" r="7.5" fill="#7fd4ff"/>
            <circle class="recDot" cx="76" cy="83" r="4"/>
            <rect x="100" y="112" width="13" height="32" fill="#8ea5cc"/>
            <rect x="38" y="142" width="134" height="11" rx="5.5" fill="#8ea5cc"/>
            <rect x="248" y="126" width="126" height="128" rx="18" fill="#061940" stroke="#f4f8ff" stroke-width="4"/>
            <g fill="#17477a">
              <rect x="262" y="142" width="46" height="44" rx="5"/>
              <rect x="316" y="142" width="46" height="44" rx="5"/>
              <rect x="262" y="194" width="46" height="44" rx="5"/>
              <rect x="316" y="194" width="46" height="44" rx="5"/>
            </g>
            <g fill="#2e86de" opacity=".55">
              <rect x="262" y="142" width="46" height="10" rx="3"/>
              <rect x="316" y="194" width="46" height="10" rx="3"/>
            </g>
            <circle class="recDot" cx="270" cy="151" r="3.4"/>
          </svg>
          <div class="scene-cap">
            <span class="live"><i></i> Pantau dari HP, 24 jam</span>
            <b>Setting DVR/NVR</b>
          </div>
        </div>
      </div>
    </div>
  </div>
</section>

{blok_trust()}

{blok_kartu_layanan()}

{blok_rating()}

{blok_keunggulan()}

{blok_kartu_area()}

{blok_faq(DATA['faq_umum'])}

{blok_cta()}"""

    schema = f"""<script type="application/ld+json">
{schema_bisnis()}
</script>
{schema_faq(DATA['faq_umum'])}"""

    jejak_home = [("Beranda", "")]
    schema = (schema_website() + "\n" + schema + "\n"
              + schema_breadcrumb(jejak_home))

    return halaman(judul, desk, isi, aktif="Beranda", kedalaman=0,
                   canonical="", schema_extra=schema)


# ============================================================
# HALAMAN: LAYANAN
# ============================================================
def buat_layanan(l):
    isi = f"""<section class="hero-kecil">
  <div class="container">
    <div class="breadcrumb">
      <a href="{_rel('index.html')}">Beranda</a><span>/</span>
      <a href="{_rel('index.html')}#layanan">Layanan</a><span>/</span>
      {esc(l['nama'])}
    </div>
    <h1>{esc(l['nama'])}</h1>
    <p class="lede">{esc(l['deskripsi_seo'])}</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="{wa_pesan(f"Assalamualaikum {B['nama']}, saya butuh {l['nama'].lower()}.")}" target="_blank" rel="noopener">Chat WhatsApp</a>
      <a class="btn btn-outline" href="tel:+{esc(WA)}">Telepon Sekarang</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Masalah Umum</span>
      <h2>Kalau Mengalami Ini, Hubungi Kami</h2>
    </div>
    <div class="dua-kolom">
      <ul>
{''.join([f'        <li>{esc(x)}</li>' + chr(10) for x in l['masalah'][:3]])}      </ul>
      <ul>
{''.join([f'        <li>{esc(x)}</li>' + chr(10) for x in l['masalah'][3:]])}      </ul>
    </div>
  </div>
</section>

<section class="section section-abu">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Yang Kami Kerjakan</span>
      <h2>Pekerjaan {esc(l['nama'])}</h2>
    </div>
    <div class="dua-kolom">
      <ul>
{''.join([f'        <li>{esc(x)}</li>' + chr(10) for x in l['pekerjaan'][:3]])}      </ul>
      <ul>
{''.join([f'        <li>{esc(x)}</li>' + chr(10) for x in l['pekerjaan'][3:]])}      </ul>
    </div>
    <div class="kotak-info" style="max-width:900px;margin-left:auto;margin-right:auto">
      <p><strong>Area layanan:</strong> Solo (Surakarta), Sukoharjo, dan Karanganyar. Untuk wilayah lain di sekitar Solo Raya, silakan tanya dulu.</p>
    </div>
  </div>
</section>

{blok_keunggulan()}

{blok_faq(l['faq'], f"Pertanyaan Seputar {l['nama']}")}

{blok_cta(f"Butuh {l['nama'].lower()} hari ini?")}"""

    jejak = [("Beranda", ""), (l['nama'], f"layanan/{l['slug']}.html")]
    schema = schema_bisnis() + "\n" + schema_layanan(l) + "\n" + schema_breadcrumb(jejak) + "\n" + schema_faq(l['faq'])

    return halaman(l['judul_seo'], l['deskripsi_seo'], isi, aktif=l['nama'],
                   kedalaman=1, canonical=f"layanan/{l['slug']}.html",
                   schema_extra=schema)


# ============================================================
# HALAMAN: AREA
# ============================================================
def buat_area(a):
    judul = f"Servis AC & Pasang CCTV {a['nama_lengkap']} | {B['nama']}"
    desk = f"Jasa servis AC dan pemasangan CCTV di {a['nama_lengkap']}. Melayani {', '.join(a['kecamatan'][:5])}, dan sekitarnya. Teknisi datang ke lokasi, bergaransi."

    daftar_layanan = ""
    for l in DATA["layanan"]:
        daftar_layanan += f"""        <li><a href="{_rel('layanan/' + l['slug'] + '.html')}">{esc(l['nama'])} di {esc(a['nama'])}</a></li>
"""

    kec_list = "\n".join([f'        <li>{esc(k)}</li>' for k in a['kecamatan']])

    # FAQ khusus area
    faq_area = [
        {"q": f"Apakah melayani {a['nama']}?", "a": f"Ya. Kami melayani seluruh wilayah {a['nama_lengkap']}, termasuk {', '.join(a['kecamatan'][:4])}, dan kecamatan lainnya."},
        {"q": f"Berapa lama teknisi sampai di {a['nama']}?", "a": f"Tergantung jarak dan antrian. Untuk wilayah {a['nama']}, biasanya bisa dijadwalkan di hari yang sama. Hubungi kami dulu untuk memastikan."},
        {"q": f"Apakah ada biaya survei ke {a['nama']}?", "a": "Untuk wilayah Solo Raya termasuk " + a['nama'] + ", survei dan konsultasi tidak dikenakan biaya."},
    ] + DATA['faq_umum'][2:4]

    isi = f"""<section class="hero-kecil">
  <div class="container">
    <div class="breadcrumb">
      <a href="{_rel('index.html')}">Beranda</a><span>/</span>
      <a href="{_rel('index.html')}#area">Area</a><span>/</span>
      {esc(a['nama'])}
    </div>
    <h1>Servis AC &amp; Pasang CCTV di {esc(a['nama'])}</h1>
    <p class="lede">{esc(a['catatan'])}</p>
    <div class="hero-cta">
      <a class="btn btn-wa" href="{wa_pesan(f"Assalamualaikum {B['nama']}, saya di {a['nama']} dan butuh bantuan AC/CCTV.")}" target="_blank" rel="noopener">Chat WhatsApp</a>
      <a class="btn btn-outline" href="tel:+{esc(WA)}">Telepon {esc(B['telepon_display'])}</a>
    </div>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Cakupan Wilayah</span>
      <h2>Kecamatan yang Kami Layani di {esc(a['nama'])}</h2>
      <p>{esc(a['catatan'])}</p>
    </div>
    <div class="dua-kolom">
      <ul>
{chr(10).join(['        <li>' + esc(k) + '</li>' for k in a['kecamatan'][:6]])}
      </ul>
      <ul>
{chr(10).join(['        <li>' + esc(k) + '</li>' for k in a['kecamatan'][6:]])}
      </ul>
    </div>
  </div>
</section>

<section class="section section-abu">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Layanan</span>
      <h2>Layanan Tersedia di {esc(a['nama'])}</h2>
    </div>
    <div class="dua-kolom" style="max-width:600px">
      <ul>
{daftar_layanan}      </ul>
    </div>
  </div>
</section>

{blok_rating()}

{blok_keunggulan()}

{blok_faq(faq_area, f"Pertanyaan Seputar Layanan di {a['nama']}")}

{blok_cta(f"Butuh teknisi di {a['nama']} hari ini?", f"Hubungi {B['nama']}. Kami siap datang ke lokasi Anda di {a['nama']} dan sekitarnya.")}"""

    jejak = [("Beranda", ""), ("Area", "index.html#area"), (a['nama'], f"area/{a['slug']}.html")]
    schema = (schema_bisnis() + "\n" + schema_area(a) + "\n"
              + schema_breadcrumb(jejak) + "\n" + schema_faq(faq_area))

    return halaman(judul, desk, isi, aktif="Area", kedalaman=1,
                   canonical=f"area/{a['slug']}.html", schema_extra=schema)


# ============================================================
# HALAMAN: KONTAK
# ============================================================
def buat_kontak():
    judul = f"Hubungi {B['nama']} — Servis AC & CCTV Solo Raya"
    desk = f"Cara menghubungi {B['nama']}. WhatsApp {B['telepon_display']}. Melayani Solo, Sukoharjo, Karanganyar. Respon cepat, survei gratis."

    isi = f"""<section class="hero-kecil">
  <div class="container">
    <div class="breadcrumb">
      <a href="{_rel('index.html')}">Beranda</a><span>/</span>
      Kontak
    </div>
    <h1>Hubungi Kami</h1>
    <p class="lede">Pilih cara yang paling nyaman untuk Anda. Kami respon secepatnya.</p>
  </div>
</section>

<section class="section">
  <div class="container">
    <div class="info-kontak">
      <div class="info-item">
        <div class="ikon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="#25d366" aria-hidden="true"><path d="M12 2a10 10 0 00-8.6 15L2 22l5.2-1.4A10 10 0 1012 2zm0 2a8 8 0 016.9 12l-.4.6 1 3.5-3.6-1-.6.4A8 8 0 1112 4zm-3.3 4c-.2 0-.5.1-.7.4-.3.3-.9 1-.9 2s.7 2.1.8 2.2c.1.2 1.4 2.2 3.4 3 1.7.7 2 .6 2.4.5.4 0 1.2-.4 1.4-1 .2-.5.2-1 .1-1.1 0-.1-.2-.2-.4-.3l-1.4-.7c-.2-.1-.4-.1-.5.1l-.6.8c-.1.2-.3.2-.5.1-.2-.1-.9-.4-1.7-1.1-.6-.6-1-1.2-1.1-1.4-.1-.2 0-.4.1-.5l.4-.5c.1-.2.2-.3.3-.5 0-.2 0-.3-.1-.4l-.6-1.5c-.2-.4-.3-.4-.5-.4z"/></svg>
        </div>
        <h4>WhatsApp</h4>
        <p><a href="{wa_pesan(f"Assalamualaikum {B['nama']}, saya ingin konsultasi.")}" target="_blank" rel="noopener">{esc(B['telepon_display'])}</a></p>
      </div>
      <div class="info-item">
        <div class="ikon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1c5fb0" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><path d="M4 5h4l2 5-2.5 1.5a11 11 0 005 5L14 14l5 2v4a1 1 0 01-1 1A16 16 0 013 6a1 1 0 011-1z"/></svg>
        </div>
        <h4>Telepon</h4>
        <p><a href="tel:+{esc(WA)}">{esc(B['telepon_display'])}</a></p>
      </div>
      <div class="info-item">
        <div class="ikon">
          <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="#1c5fb0" stroke-width="1.9" stroke-linecap="round" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
        </div>
        <h4>Jam Kerja</h4>
        <p>{esc(B['jam_kerja'])}</p>
      </div>
    </div>

    <div class="kotak-info" style="max-width:900px;margin:40px auto 0">
      <p><strong>Area layanan:</strong> Solo (Surakarta), Sukoharjo, dan Karanganyar. Untuk wilayah sekitar Solo Raya, silakan tanya dulu lewat WhatsApp.</p>
    </div>
  </div>
</section>

<section class="section section-abu">
  <div class="container">
    <div class="section-title">
      <span class="kicker">Cara Pesan</span>
      <h2>Langkah Mudah Pesan Layanan</h2>
    </div>
    <div class="dua-kolom" style="max-width:800px">
      <ul>
        <li>Hubungi kami lewat WhatsApp atau telepon</li>
        <li>Sebutkan layanan yang dibutuhkan</li>
        <li>Sebutkan lokasi Anda</li>
        <li>Kami jadwalkan kunjungan teknisi</li>
      </ul>
      <ul>
        <li>Teknisi datang ke lokasi</li>
        <li>Pengecekan dan penjelasan biaya</li>
        <li>Pekerjaan dikerjakan setelah Anda setuju</li>
        <li>Pembayaran setelah selesai dan Anda cek hasilnya</li>
      </ul>
    </div>
  </div>
</section>

{blok_faq(DATA['faq_umum'])}

{blok_cta("Masih ada pertanyaan?", "Chat kami sekarang. Kami bantu jawab dulu, gratis.")}"""

    jejak = [("Beranda", ""), ("Kontak", "kontak.html")]
    schema = schema_breadcrumb(jejak) + "\n" + schema_faq(DATA['faq_umum'])

    jejak_kontak = [("Beranda", ""), ("Kontak", "kontak.html")]
    schema = (schema_bisnis() + "\n" + schema_kontak() + "\n"
              + schema_breadcrumb(jejak_kontak))

    return halaman(judul, desk, isi, aktif="Kontak", kedalaman=0,
                   canonical="kontak.html", schema_extra=schema)


# ============================================================
# FILE TAMBAHAN: robots.txt & sitemap.xml
# ============================================================
def buat_robots():
    return f"""# robots.txt — {B['nama']}
User-agent: *
Allow: /

# AI crawler (untuk GEO — muncul di ChatGPT, Gemini, Perplexity)
User-agent: GPTBot
Allow: /

User-agent: ChatGPT-User
Allow: /

User-agent: Google-Extended
Allow: /

User-agent: PerplexityBot
Allow: /

User-agent: ClaudeBot
Allow: /

User-agent: anthropic-ai
Allow: /

User-agent: CCBot
Allow: /

# AI crawler tambahan
User-agent: GoogleOther
Allow: /

User-agent: Applebot-Extended
Allow: /

User-agent: meta-externalagent
Allow: /

User-agent: Bytespider
Allow: /

# Sitemap
Sitemap: {DOMAIN}/sitemap.xml
"""


def buat_sitemap():
    hari = date.today().isoformat()
    url = [("", "1.0", "weekly")]
    for l in DATA["layanan"]:
        url.append((f"layanan/{l['slug']}.html", "0.9", "monthly"))
    for a in DATA["area"]:
        url.append((f"area/{a['slug']}.html", "0.8", "monthly"))
    url.append(("kontak.html", "0.7", "monthly"))

    def satu(u, p, c):
        loc = f"{DOMAIN}/{u}" if u else f"{DOMAIN}/"
        # Gambar ikut didaftarkan (bantu Google Images & preview)
        img = ""
        if u == "":
            img = f"""
    <image:image>
      <image:loc>{DOMAIN}/og-cover.png</image:loc>
      <image:title>{esc(B['nama_resmi'])}</image:title>
    </image:image>"""
        return f"""  <url>
    <loc>{loc}</loc>
    <lastmod>{hari}</lastmod>
    <changefreq>{c}</changefreq>
    <priority>{p}</priority>{img}
  </url>"""

    item = "\n".join([satu(u, p, c) for u, p, c in url])

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        xmlns:image="http://www.google.com/schemas/sitemap-image/1.1"
        xmlns:xhtml="http://www.w3.org/1999/xhtml">
{item}
</urlset>
"""


# ============================================================
# JALANKAN
# ============================================================
def main():
    print("=" * 62)
    print(f"  GENERATOR WEBSITE {B['nama']}")
    print("=" * 62)

    (BASE / "layanan").mkdir(exist_ok=True)
    (BASE / "area").mkdir(exist_ok=True)

    daftar = []

    # Beranda
    (BASE / "index.html").write_text(buat_beranda(), encoding="utf-8")
    daftar.append(("index.html", "beranda"))

    # Layanan
    for l in DATA["layanan"]:
        f = BASE / "layanan" / f"{l['slug']}.html"
        f.write_text(buat_layanan(l), encoding="utf-8")
        daftar.append((f"layanan/{l['slug']}.html", l['nama']))

    # Area
    for a in DATA["area"]:
        f = BASE / "area" / f"{a['slug']}.html"
        f.write_text(buat_area(a), encoding="utf-8")
        daftar.append((f"area/{a['slug']}.html", a['nama']))

    # Kontak
    (BASE / "kontak.html").write_text(buat_kontak(), encoding="utf-8")
    daftar.append(("kontak.html", "kontak"))

    # SEO files
    (BASE / "robots.txt").write_text(buat_robots(), encoding="utf-8")
    daftar.append(("robots.txt", "SEO"))
    (BASE / "sitemap.xml").write_text(buat_sitemap(), encoding="utf-8")
    daftar.append(("sitemap.xml", "SEO"))

    print(f"\n✅ {len(daftar)} halaman dibuat:\n")
    for f, ket in daftar:
        p = BASE / f
        ukuran = p.stat().st_size if p.exists() else 0
        print(f"   {f:34} {ukuran:>8,} bytes   {ket}")

    total = sum((BASE / f).stat().st_size for f, _ in daftar if (BASE / f).exists())
    print(f"\n   Total: {total:,} bytes")


if __name__ == "__main__":
    main()
