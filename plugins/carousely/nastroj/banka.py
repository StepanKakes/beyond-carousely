"""Postaví fotobanku klienta z roztříděného seznamu.
Použití: python3 banka.py <zdrojová_složka> <cílová_složka_fotky> <seznam.tsv>
seznam.tsv: řádky  soubor|kategorie|nazev|popis a tip na použití
Kategorie: portrety, prace, lifestyle, pribeh, rodina, detaily. Nic se nemaže, HEIC se převede na JPEG.
Výstup: <cíl>/<kategorie>/<kategorie>_<nazev>.jpg a <cíl>/katalog.md
"""
import os, subprocess, shutil, sys
from PIL import Image, ImageOps
src, dst, seznam = sys.argv[1:4]
radky = [r.split("|", 3) for r in open(seznam, encoding="utf-8").read().strip().splitlines() if r.strip() and not r.startswith("#")]
kat = {}
for soubor, sl, nazev, popis in radky:
    os.makedirs(os.path.join(dst, sl), exist_ok=True)
    cil = os.path.join(dst, sl, f"{sl}_{nazev}.jpg")
    z = os.path.join(src, soubor)
    if soubor.lower().endswith(".heic") and shutil.which("sips"):
        subprocess.run(["sips", "-s", "format", "jpeg", z, "--out", cil], check=True, capture_output=True)
    else:
        if soubor.lower().endswith(".heic"):
            import pillow_heif; pillow_heif.register_heif_opener()
        im = Image.open(z); im = ImageOps.exif_transpose(im).convert("RGB"); im.save(cil, quality=92)
    kat.setdefault(sl, []).append(f"- `{sl}/{os.path.basename(cil)}`: {popis}")
with open(os.path.join(dst, "katalog.md"), "w", encoding="utf-8") as f:
    f.write("# Fotobanka\n\nNic se nemaže. Ukazující a pózující fotky jen na hook a CTA.\n")
    for sl, r in kat.items():
        f.write(f"\n## {sl} ({len(r)})\n\n" + "\n".join(r) + "\n")
print(sum(len(r) for r in kat.values()), "fotek ->", dst)
