# -*- coding: utf-8 -*-
"""
Favicon BULAT untuk ARTA TEKNIK - versi tajam.

Sumber: img/logo-ikon.png (1390x836, sudah transparan & putih)
Ikon putih diletakkan di dalam lingkaran navy.
"""
from PIL import Image, ImageDraw
import numpy as np
from pathlib import Path

BASE = Path(r"C:\Users\HI\arta-website")
SUMBER = BASE / "img" / "logo-ikon.png"
OUT = BASE / "img"
OUT.mkdir(exist_ok=True)

# ---- 1. Ambil ikon putih (sudah transparan) ----
ikon = Image.open(SUMBER).convert("RGBA")
a = np.array(ikon)
al = a[:, :, 3]
bar = np.where((al > 20).any(axis=1))[0]
kol = np.where((al > 20).any(axis=0))[0]
ikon = ikon.crop((kol.min(), bar.min(), kol.max() + 1, bar.max() + 1))
print(f"ikon sumber: {ikon.size[0]}x{ikon.size[1]} (tajam)")

# versi navy dari bentuk ikon (untuk latar terang)
aa = np.array(ikon)
navy = np.zeros_like(aa)
navy[:, :, 0] = 11
navy[:, :, 1] = 42
navy[:, :, 2] = 78
navy[:, :, 3] = aa[:, :, 3]
ikon_navy = Image.fromarray(navy, "RGBA")


def dalam_lingkaran(isi, warna_bg, ukuran=256, isi_rasio=0.58):
    """Ikon di tengah lingkaran. Render besar dulu supaya tepi halus."""
    S = 1024
    kanvas = Image.new("RGBA", (S, S), (0, 0, 0, 0))
    d = ImageDraw.Draw(kanvas)

    if isinstance(warna_bg[0], tuple):
        c1, c2 = warna_bg
        for y in range(S):
            t = y / S
            c = tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)) + (255,)
            d.line([(0, y), (S, y)], fill=c)
    else:
        d.ellipse([0, 0, S - 1, S - 1], fill=warna_bg + (255,))

    # potong jadi lingkaran (mask)
    mask = Image.new("L", (S, S), 0)
    ImageDraw.Draw(mask).ellipse([0, 0, S - 1, S - 1], fill=255)
    kanvas.putalpha(mask)

    # perbesar ikon sesuai rasio
    target = int(S * isi_rasio)
    rasio = isi.size[1] / isi.size[0]
    if rasio <= 1:
        w, h = target, max(1, int(target * rasio))
    else:
        h, w = target, max(1, int(target / rasio))
    ik = isi.resize((w, h), Image.LANCZOS)
    kanvas.alpha_composite(ik, ((S - w) // 2, (S - h) // 2))
    return kanvas.resize((ukuran, ukuran), Image.LANCZOS)


NAVY = (11, 42, 78)
EMAS = ((248, 196, 32), (214, 148, 0))

varian = {
    "navy": dalam_lingkaran(ikon, NAVY),
    "putih": dalam_lingkaran(ikon_navy, (255, 255, 255)),
    "emas": dalam_lingkaran(ikon_navy, EMAS),
}

for nama, img in varian.items():
    img.save(OUT / f"favicon-bulat-{nama}.png", optimize=True)
    img.resize((180, 180), Image.LANCZOS).save(OUT / f"favicon-bulat-{nama}-180.png", optimize=True)
    img.resize((32, 32), Image.LANCZOS).save(OUT / f"favicon-bulat-{nama}-32.png", optimize=True)
    print(f"  favicon-bulat-{nama}.png  256 + 180 + 32 px")

# ---- verifikasi teknis ----
print("\nverifikasi (lingkaran sejati = sudut transparan):")
for nama in varian:
    im = Image.open(OUT / f"favicon-bulat-{nama}.png").convert("RGBA")
    b = np.array(im)
    al = b[:, :, 3]
    S = im.size[0]
    sudut = [al[2, 2], al[2, S - 3], al[S - 3, 2], al[S - 3, S - 3]]
    semi = ((al > 10) & (al < 245)).sum()
    print(f"  {nama:6} sudut alpha={sudut}  antialias={semi:,} px")

# preview untuk dicek mata (tetap, tidak bergerigi)
besar = Image.new("RGB", (256 * 3 + 80, 296), (238, 240, 244))
x = 20
for nama in varian:
    im = Image.open(OUT / f"favicon-bulat-{nama}.png").convert("RGB")
    besar.paste(im, (x, 20))
    x += 256 + 20
besar.save(Path(r"C:\Users\HI\AppData\Local\Temp\fav") / "final_256.png")
print("\npreview -> final_256.png")
