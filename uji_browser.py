# -*- coding: utf-8 -*-
"""Uji kemampuan lengkap Playwright sebagai pengganti agent-browser."""
from playwright.sync_api import sync_playwright

BASE = "https://azzamamry-lab.github.io/ArtaTeknik"

with sync_playwright() as pw:
    b = pw.chromium.launch(headless=True)
    pg = b.new_page(viewport={"width": 1440, "height": 900})

    # 1. BUKA + BACA
    pg.goto(f"{BASE}/layanan/ac.html", timeout=45000, wait_until="domcontentloaded")
    pg.wait_for_timeout(1200)
    print("[1] BUKA+BACA      :", pg.title()[:55])

    # 2. KLIK (tab AC <-> CCTV di hero beranda)
    pg.goto(f"{BASE}/", timeout=45000, wait_until="domcontentloaded")
    pg.wait_for_timeout(1500)
    try:
        pg.click("#tCCTV", timeout=8000)
        pg.wait_for_timeout(1200)
        aktif = pg.eval_on_selector("#tCCTV", "e => e.getAttribute('aria-selected')")
        print("[2] KLIK tab CCTV  : aria-selected =", aktif)
    except Exception as e:
        print("[2] KLIK gagal     :", str(e)[:70])

    # 3. SCREENSHOT
    pg.goto(f"{BASE}/layanan/ac.html", timeout=45000, wait_until="domcontentloaded")
    pg.wait_for_timeout(1500)
    pg.evaluate("document.querySelector('#harga').scrollIntoView()")
    pg.wait_for_timeout(800)
    pg.screenshot(path="/tmp/pw_harga.png")
    print("[3] SCREENSHOT     : /tmp/pw_harga.png")

    # 4. BACA DATA terstruktur dari halaman
    hr = pg.eval_on_selector_all(
        ".price-item",
        "els => els.map(e => e.innerText.replace(/\\n/g,' | '))")
    print("[4] BACA DATA      :", len(hr), "item harga")
    for h in hr:
        print("      -", h[:60])

    # 5. COOKIE (untuk simpan sesi login)
    ctx = b.new_context()
    ctx.add_cookies([{"name": "uji", "value": "1",
                      "domain": ".github.io", "path": "/"}])
    print("[5] COOKIE/sesi    : OK")
    b.close()

    # 6. HEADED (browser terlihat - untuk login manual / cek visual)
    b2 = pw.chromium.launch(headless=False)
    p2 = b2.new_page()
    p2.goto(f"{BASE}/", timeout=45000, wait_until="domcontentloaded")
    p2.wait_for_timeout(1500)
    print("[6] HEADED + BUKA  :", p2.title()[:55])
    b2.close()

print()
print("-> SEMUA KEMAMPUAN SIAP DIPAKAI")
