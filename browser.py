#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
browser.py — alat browser andal untuk ARTA TEKNIK (dan web pada umumnya).

KENAPA INI ADA:
agent-browser CLI menggantung di komputer ini (shim shell npm macet, dan
sesinya mati saat shell keluar). Playwright yang sudah terinstall terbukti
jalan sempurna. Jadi pakai ini.

PAKAI:
  python browser.py buka  <url>                 # buka & tampilkan ringkasan
  python browser.py teks  <url>                 # ambil teks halaman
  python browser.py elemen <url> <selector>     # teks semua elemen tertentu
  python browser.py gambar <url> <file.png>     # screenshot
  python browser.py uji   <url>                 # laporan kesehatan halaman
  python browser.py isi   <url> <sel> <teks>    # isi input
  python browser.py klik  <url> <selector>      # klik elemen
"""
import sys
import json
from playwright.sync_api import sync_playwright

UA = ("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
      "(KHTML, like Gecko) Chrome/155.0.0.0 Safari/537.36")


def jalan(fn, headless=True, lebar=1440, tinggi=900):
    with sync_playwright() as pw:
        b = pw.chromium.launch(headless=headless)
        ctx = b.new_context(
            viewport={"width": lebar, "height": tinggi},
            user_agent=UA,
        )
        pg = ctx.new_page()
        try:
            return fn(pg)
        finally:
            b.close()


def ringkas(pg, url):
    pg.goto(url, timeout=45000, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)

    def aman(js, default=None):
        try:
            return pg.evaluate(js)
        except Exception:
            return default

    data = {
        "judul": pg.title(),
        "url_akhir": pg.url,
        "teks_panjang": len(aman("document.body.innerText || ''", "")),
        "h1": aman("Array.from(document.querySelectorAll('h1')).map(e=>e.textContent.trim())", []),
        "h2": aman("Array.from(document.querySelectorAll('h2')).map(e=>e.textContent.trim())", []),
        "menu": aman("Array.from(document.querySelectorAll('nav a')).map(e=>e.textContent.trim())", []),
        "link": aman("document.querySelectorAll('a').length", 0),
        "gambar": aman("Array.from(document.images).map(i=>({src:i.currentSrc||i.src,ok:i.naturalWidth>0}))", []),
        "wa": aman("Array.from(document.querySelectorAll('a[href*=\"wa.me\"]')).map(e=>e.href)", []),
        "error_js": aman("window.__err || 0", 0),
    }
    return data


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        return 1

    cmd, url = sys.argv[1], sys.argv[2]

    if cmd == "buka":
        d = jalan(lambda pg: ringkas(pg, url))
        print(json.dumps(d, indent=2, ensure_ascii=False)[:4000])

    elif cmd == "teks":
        t = jalan(lambda pg: (pg.goto(url, timeout=45000, wait_until="domcontentloaded"),
                              pg.wait_for_timeout(1000),
                              pg.inner_text("body"))[2])
        print(t[:6000])

    elif cmd == "elemen":
        sel = sys.argv[3]
        out = jalan(lambda pg: (pg.goto(url, timeout=45000, wait_until="domcontentloaded"),
                                pg.wait_for_timeout(1000),
                                pg.eval_on_selector_all(
                                    sel, "els => els.map(e => e.textContent.trim())"))[2])
        for i, x in enumerate(out, 1):
            print(f"{i}. {x}")

    elif cmd == "gambar":
        keluar = sys.argv[3]
        jalan(lambda pg: (pg.goto(url, timeout=45000, wait_until="domcontentloaded"),
                          pg.wait_for_timeout(1500),
                          pg.screenshot(path=keluar, full_page=True))[2], )
        print(f"screenshot -> {keluar}")

    elif cmd == "klik":
        sel = sys.argv[3]
        def aksi(pg):
            pg.goto(url, timeout=45000, wait_until="domcontentloaded")
            pg.wait_for_timeout(1200)
            pg.click(sel, timeout=15000)
            pg.wait_for_timeout(1500)
            return f"klik '{sel}' OK | url sekarang: {pg.url}"
        print(jalan(aksi))

    elif cmd == "isi":
        sel, teks = sys.argv[3], sys.argv[4]
        def aksi(pg):
            pg.goto(url, timeout=45000, wait_until="domcontentloaded")
            pg.wait_for_timeout(1200)
            pg.fill(sel, teks, timeout=15000)
            return f"isi '{sel}' OK"
        print(jalan(aksi))

    elif cmd == "uji":
        d = jalan(lambda pg: ringkas(pg, url))
        print("=" * 60)
        print(f"  UJI HALAMAN: {d['url_akhir']}")
        print("=" * 60)
        print(f"  judul   : {d['judul']}")
        print(f"  teks    : {d['teks_panjang']} karakter terlihat")
        print(f"  h1      : {len(d['h1'])} -> {d['h1']}")
        print(f"  h2      : {len(d['h2'])}")
        print(f"  menu    : {' | '.join(d['menu'][:10])}")
        print(f"  link    : {d['link']}")
        print(f"  WA      : {len(d['wa'])} tombol")
        rusak = [g["src"] for g in d["gambar"] if not g["ok"]]
        print(f"  gambar  : {len(d['gambar'])} total, {len(rusak)} GAGAL muat")
        for g in rusak[:8]:
            print(f"      RUSAK: {g}")
        # deteksi halaman tampil mentah (JSON bocor)
        mentah = any('"@context"' in h for h in d["h1"])
        print(f"  status  : {'RUSAK (JSON bocor)' if mentah else 'OK'}")
        return 0 if not rusak and not mentah else 1

    else:
        print(__doc__)
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
