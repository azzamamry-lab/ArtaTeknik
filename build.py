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

# Domain nanti diisi setelah beli
DOMAIN = "https://artatehnik.com"

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
# TEMPLATE KOMPONEN
# ============================================================
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

    return f"""<!DOCTYPE html>
<html lang="id">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{esc(judul)}</title>
<meta name="description" content="{esc(deskripsi)}">
<meta name="robots" content="index, follow, max-image-preview:large">
<link rel="canonical" href="{canon}">

<!-- Open Graph -->
<meta property="og:type" content="website">
<meta property="og:site_name" content="{esc(B['nama'])}">
<meta property="og:title" content="{esc(judul)}">
<meta property="og:description" content="{esc(deskripsi)}">
<meta property="og:url" content="{canon}">
<meta property="og:image" content="{DOMAIN}/{og_gambar}">
<meta property="og:locale" content="id_ID">

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
</style>
{schema_extra}
</head>
<body>
{head_final}
{isi_final}
{foot_final}
{skrip()}
</body>
</html>"""


# ============================================================
# SCHEMA JSON-LD
# ============================================================
def schema_bisnis():
    area = ", ".join([f"{a['nama']}" for a in DATA["area"]])
    return f"""{{
  "@context": "https://schema.org",
  "@type": "HVACBusiness",
  "@id": "{DOMAIN}/#bisnis",
  "name": "{esc(B['nama'])}",
  "description": "{esc(B['deskripsi'])} di {esc(area)}.",
  "url": "{DOMAIN}/",
  "telephone": "+{esc(WA)}",
  "priceRange": "Rp",
  "image": "{DOMAIN}/og-cover.png",
  "address": {{
    "@type": "PostalAddress",
    "addressRegion": "{esc(B['alamat']['region'])}",
    "addressCountry": "{esc(B['alamat']['negara'])}"
  }},
  "areaServed": [
{', '.join([f'    {{"@type": "City", "name": "{esc(a["nama_lengkap"])}"}}' for a in DATA["area"]])}
  ],
  "openingHoursSpecification": {{
    "@type": "OpeningHoursSpecification",
    "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday"],
    "opens": "08:00",
    "closes": "20:00"
  }},
  "hasOfferCatalog": {{
    "@type": "OfferCatalog",
    "name": "Layanan {esc(B['nama'])}",
    "itemListElement": [
{', '.join([f'''      {{"@type": "Offer", "itemOffered": {{"@type": "Service", "name": "{esc(l['nama'])}", "url": "{DOMAIN}/layanan/{l['slug']}.html"}}}}''' for l in DATA["layanan"]])}
    ]
  }}
}}"""


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
    return f"""<script type="application/ld+json">
{{
  "@context": "https://schema.org",
  "@type": "Service",
  "serviceType": "{esc(l['nama'])}",
  "provider": {{"@id": "{DOMAIN}/#bisnis"}},
  "areaServed": [
{', '.join([f'    {{"@type": "City", "name": "{esc(a["nama_lengkap"])}"}}' for a in DATA["area"]])}
  ],
  "description": "{esc(l['deskripsi_seo'])}",
  "url": "{DOMAIN}/layanan/{l['slug']}.html"
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
    for k in DATA["keunggulan"]:
        kartu += f"""      <div class="keunggulan-item">
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
    for l in DATA["layanan"]:
        kartu += f"""      <article class="kartu-l">
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
    for a in DATA["area"]:
        kec = ", ".join(a["kecamatan"][:6])
        sisa = len(a["kecamatan"]) - 6
        if sisa > 0:
            kec += f", dan {sisa} kecamatan lain"
        kartu += f"""      <article class="area-kartu">
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
def buat_beranda():
    judul = f"{B['nama']} — Spesialis AC & CCTV | Solo, Sukoharjo, Karanganyar"
    desk = f"{B['nama']}, spesialis pemasangan, servis, dan perawatan AC & CCTV di Solo, Sukoharjo, Karanganyar. Teknisi berpengalaman, bergaransi, harga bersahabat."

    isi = f"""<section class="hero">
  <div class="hero-grid-lines"></div>
  <div class="container hero-inner">
    <div>
      <span class="hero-badge">
        <span class="dot"></span> Spesialis AC &amp; CCTV
      </span>
      <h1>AC Tidak Dingin?<br>Rumah Belum Aman?</h1>
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
      <div class="mini-icons">
        <span><b>Respon cepat</b> Bisa hari ini</span>
        <span><b>Garansi</b> Setiap pekerjaan</span>
      </div>
    </div>
    <div class="hero-poin">
      <div class="hp">
        <b>Aman &amp; Terpercaya</b>
        <span>Sudah dipercaya pelanggan Solo Raya</span>
      </div>
      <div class="hp">
        <b>Profesional</b>
        <span>Teknisi berpengalaman dan teliti</span>
      </div>
      <div class="hp">
        <b>Bergaransi</b>
        <span>Setiap pekerjaan ada garansi</span>
      </div>
      <div class="hp">
        <b>Harga Bersahabat</b>
        <span>Transparan, tanpa biaya dadakan</span>
      </div>
    </div>
  </div>
</section>

{blok_kartu_layanan()}

{blok_keunggulan()}

{blok_kartu_area()}

{blok_faq(DATA['faq_umum'])}

{blok_cta()}"""

    schema = f"""<script type="application/ld+json">
{schema_bisnis()}
</script>
{schema_faq(DATA['faq_umum'])}"""

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
    schema = schema_layanan(l) + "\n" + schema_breadcrumb(jejak) + "\n" + schema_faq(l['faq'])

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

{blok_keunggulan()}

{blok_faq(faq_area, f"Pertanyaan Seputar Layanan di {a['nama']}")}

{blok_cta(f"Butuh teknisi di {a['nama']} hari ini?", f"Hubungi {B['nama']}. Kami siap datang ke lokasi Anda di {a['nama']} dan sekitarnya.")}"""

    jejak = [("Beranda", ""), (a['nama'], f"area/{a['slug']}.html")]
    schema = schema_breadcrumb(jejak) + "\n" + schema_faq(faq_area)

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

    item = "\n".join([f"""  <url>
    <loc>{DOMAIN}/{u}</loc>
    <lastmod>{hari}</lastmod>
    <changefreq>{c}</changefreq>
    <priority>{p}</priority>
  </url>""" for u, p, c in url])

    return f"""<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
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
