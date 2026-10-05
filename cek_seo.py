# -*- coding: utf-8 -*-
"""Validasi SEO/GEO menyeluruh untuk semua halaman ARTA TEKNIK."""
import json, re, sys
from pathlib import Path
from html.parser import HTMLParser

BASE = Path(__file__).parent
hal = ["index.html", "layanan/servis-ac.html", "layanan/pasang-ac.html",
       "layanan/pasang-cctv.html", "area/solo.html", "area/sukoharjo.html",
       "area/karanganyar.html", "kontak.html"]

VOID = {'meta','link','img','br','hr','input','source','rect','circle','path',
        'text','stop','use','area','base','col','embed','param','track','wbr',
        'ellipse','polygon','line','g','linearGradient','defs'}

masalah_total = []
ringkas = []

for h in hal:
    f = BASE / h
    src = f.read_text(encoding="utf-8")
    err = []

    # --- 1. JSON-LD valid? ---
    blok = re.findall(r'<script type="application/ld\+json">(.*?)</script>', src, re.S)
    tipe = []
    for i, b in enumerate(blok, 1):
        try:
            d = json.loads(b)
            t = d.get("@type")
            tipe.append(t if isinstance(t, str) else "/".join(t) if t else "?")
        except Exception as e:
            err.append(f"JSON-LD #{i} TIDAK VALID: {e}")

    # --- 2. Tag wajib ada? ---
    wajib = {
        'canonical': r'<link rel="canonical" href="([^"]+)"',
        'og:image': r'<meta property="og:image" content="([^"]+)"',
        'geo.region': r'<meta name="geo.region" content="([^"]+)"',
        'ICBM': r'<meta name="ICBM" content="([^"]+)"',
        'favicon': r'<link rel="icon"[^>]*href="([^"]+)"',
        'manifest': r'<link rel="manifest" href="([^"]+)"',
        'description': r'<meta name="description" content="([^"]+)"',
    }
    ada = {}
    for k, pola in wajib.items():
        m = re.search(pola, src)
        ada[k] = m.group(1) if m else None
        if not m:
            err.append(f"tag '{k}' HILANG")

    # --- 3. canonical TIDAK boleh menunjuk domain mati ---
    if ada['canonical'] and 'artatehnik.com' in ada['canonical']:
        err.append("canonical masih menunjuk artatehnik.com (domain mati!)")
    if ada['og:image'] and 'artatehnik.com' in ada['og:image']:
        err.append("og:image masih menunjuk artatehnik.com (404!)")

    # --- 4. cek duplikat deskripsi antar halaman ---
    # --- 5. tag tidak tertutup ---
    class P(HTMLParser):
        def __init__(self):
            super().__init__(); self.stack = []; self.e = []
        def handle_starttag(self, t, a):
            if t not in VOID: self.stack.append(t)
        def handle_endtag(self, t):
            if self.stack and self.stack[-1] == t: self.stack.pop()
            elif t in self.stack:
                while self.stack and self.stack[-1] != t: self.e.append(self.stack.pop())
                if self.stack: self.stack.pop()
    pp = P(); pp.feed(src)
    if pp.stack: err.append(f"tag tidak tertutup: {pp.stack}")
    if pp.e: err.append(f"tag error: {pp.e}")

    # --- 6. h1 harus tepat 1 ---
    n_h1 = len(re.findall(r'<h1', src))
    if n_h1 != 1: err.append(f"jumlah <h1> = {n_h1} (seharusnya 1)")

    # --- 7. jumlah kata ---
    teks = re.sub(r'<(script|style)[^>]*>.*?</\1>', ' ', src, flags=re.S)
    teks = re.sub(r'<[^>]+>', ' ', teks)
    kata = len(teks.split())

    ringkas.append({
        "halaman": h, "kata": kata, "h1": n_h1,
        "schema": ", ".join(tipe),
        "canonical": (ada['canonical'] or "").replace("https://", ""),
        "err": err,
    })
    if err: masalah_total.append((h, err))

print("=" * 78)
print("  VALIDASI SEO / GEO — ARTA TEKNIK")
print("=" * 78)
for r in ringkas:
    tanda = "OK  " if not r["err"] else "GAGAL"
    print(f"\n[{tanda}] {r['halaman']}")
    print(f"    kata       : {r['kata']}")
    print(f"    schema     : {r['schema']}")
    print(f"    canonical  : {r['canonical']}")
    for e in r["err"]:
        print(f"    !! {e}")

# --- duplikat deskripsi & title ---
print("\n" + "=" * 78)
print("  CEK DUPLIKAT (bau duplicate content)")
print("=" * 78)
desc, titles = {}, {}
for h in hal:
    src = (BASE / h).read_text(encoding="utf-8")
    d = re.search(r'<meta name="description" content="([^"]+)"', src)
    t = re.search(r'<title>([^<]+)</title>', src)
    if d: desc.setdefault(d.group(1), []).append(h)
    if t: titles.setdefault(t.group(1), []).append(h)

dub_d = {k: v for k, v in desc.items() if len(v) > 1}
dub_t = {k: v for k, v in titles.items() if len(v) > 1}
print(f"  deskripsi duplikat : {len(dub_d)}")
for k, v in dub_d.items(): print(f"     -> {v}")
print(f"  title duplikat     : {len(dub_t)}")
for k, v in dub_t.items(): print(f"     -> {v}")

# --- cek file pendukung ADA ---
print("\n" + "=" * 78)
print("  FILE PENDUKUNG")
print("=" * 78)
for f in ["og-cover.png", "favicon.svg", "site.webmanifest", "robots.txt", "sitemap.xml"]:
    p = BASE / f
    print(f"  {'ADA  ' if p.exists() else 'HILANG'} {f}" + (f"  ({p.stat().st_size} bytes)" if p.exists() else ""))

print("\n" + "=" * 78)
if masalah_total:
    print(f"  HASIL: {len(masalah_total)} halaman masih ada masalah")
    sys.exit(1)
print("  HASIL: SEMUA VALID ✅")
