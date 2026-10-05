# -*- coding: utf-8 -*-
"""Bikin og-cover.png 1200x630 untuk preview share WhatsApp/Facebook."""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

BASE = Path(__file__).parent
W, H = 1200, 630
NAVY = (11, 42, 78)
NAVY2 = (18, 58, 99)
GOLD = (245, 179, 1)
SKY = (94, 200, 240)
WHITE = (255, 255, 255)

img = Image.new("RGB", (W, H), NAVY)
d = ImageDraw.Draw(img)

# Gradien diagonal halus
for y in range(H):
    t = y / H
    r = int(NAVY[0] + (NAVY2[0] - NAVY[0]) * t)
    g = int(NAVY[1] + (NAVY2[1] - NAVY[1]) * t)
    b = int(NAVY[2] + (NAVY2[2] - NAVY[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# Aksen lingkaran glow
d.ellipse([W - 340, -160, W + 160, 340], outline=(245, 179, 1, 40), width=2)
d.ellipse([W - 280, -100, W + 100, 280], outline=(94, 200, 240, 60), width=2)

def font(size, bold=False):
    kandidat = [
        r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\segoeui.ttf",
        r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
    ]
    for k in kandidat:
        try:
            return ImageFont.truetype(k, size)
        except Exception:
            continue
    return ImageFont.load_default()

# Garis emas atas
d.rectangle([0, 0, W, 10], fill=GOLD)

# Badge kecil
d.rounded_rectangle([70, 62, 470, 118], radius=28, fill=(245, 179, 1))
d.text((92, 72), "SPESIALIS AC & CCTV", font=font(26, True), fill=NAVY)

# Judul utama
d.text((70, 160), "ARTA TEKNIK", font=font(96, True), fill=WHITE)

# Subjudul
d.text((72, 292), "Service AC & CCTV Solo Raya", font=font(44), fill=GOLD)

# Garis pemisah
d.rectangle([72, 372, 132, 378], fill=SKY)

# Baris fitur
fitur = ["Servis & Cuci AC", "Pasang AC Baru", "Pasang CCTV"]
x = 72
f = font(30, True)
for i, s in enumerate(fitur):
    w = d.textlength(s, font=f)
    d.text((x, 410), s, font=f, fill=(220, 235, 250))
    x += w + 34
    if i < len(fitur) - 1:
        d.text((x - 20, 410), "|", font=f, fill=SKY)
        x += 14

# Area + rating
d.text((72, 486), "Solo  -  Sukoharjo  -  Karanganyar", font=font(32, True), fill=WHITE)

# Badge rating — lebar otomatis mengikuti teks
teks_rating = "Rating 4.7 di Google"
fr = font(27, True)
wr = d.textlength(teks_rating, font=fr)
pad = 26
d.rounded_rectangle([72, 540, 72 + wr + pad * 2, 596], radius=26, fill=(255, 255, 255))
d.text((72 + pad, 552), teks_rating, font=fr, fill=NAVY)

# Nomor WA kanan bawah
wa = "0821-4797-5947"
fwa = font(40, True)
ww = d.textlength(wa, font=fwa)
d.text((W - ww - 72, 545), wa, font=fwa, fill=GOLD)
d.text((W - 300, 500), "Hubungi kami", font=font(26), fill=SKY)

out = BASE / "og-cover.png"
img.save(out, "PNG", optimize=True)
print(f"OK -> {out} ({out.stat().st_size} bytes, {W}x{H})")
