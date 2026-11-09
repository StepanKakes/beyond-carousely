# Seřadí fotky z banky pro půlku splitu: výřez bez zoomu, hlava celá a mimo pás textu,
# většina postavy v záběru, kontrast bílého textu v pásu uprostřed.
# Fotka s obličejem: výřez se řídí hlavou, ne kontrastem. Hlava nahoře v půlce (pod logem VS),
# text pak jde přes tělo nebo stůl s lehkým ztmavením. Nikdy postavu nestrkat ke spodnímu okraji.
# Použití: python3 pulky.py <složka_fotky> [lab_y_v_procentech, výchozí 50]
# Výpis: fotka, nejlepší y výřezu, kontrast, má obličej, má postavu (seřazeno od nejčitelnějšího).
import json, os, subprocess, sys
import numpy as np
from PIL import Image, ImageOps
F = os.path.abspath(sys.argv[1])
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from render import najdi_tvare
cache = os.path.join(F, ".tvare.json")
T = json.load(open(cache, encoding="utf-8")) if os.path.exists(cache) else {}
chybi = [f"{sl}/{f}" for sl in ("prace", "lifestyle", "portrety") if os.path.isdir(os.path.join(F, sl)) for f in os.listdir(os.path.join(F, sl)) if f.lower().endswith(".jpg") and f"{sl}/{f}" not in T]
if chybi:
    out = najdi_tvare([os.path.join(F, k) for k in chybi])
    for k in chybi: T[k] = out[os.path.join(F, k)]
    json.dump(T, open(cache, "w", encoding="utf-8"), indent=1)
LY = float(sys.argv[2]) if len(sys.argv) > 2 else 50
PAS = (int(720 * LY / 100) - 130, int(720 * LY / 100) + 130)   # pás textu v půlce 720 px (2 až 3 řádky)
out = []
for sl in ("prace", "lifestyle", "portrety"):
    if not os.path.isdir(os.path.join(F, sl)): continue
    for f in sorted(os.listdir(os.path.join(F, sl))):
        if not f.endswith(".jpg"): continue
        k = f"{sl}/{f}"
        if sl == "portrety" and not f.startswith("portrety_tmave"): continue
        im = ImageOps.exif_transpose(Image.open(os.path.join(F, k))).convert("RGB")
        w, h = im.size; s = 1080 / w; H = int(h * s)
        if H < 720: continue
        a = np.asarray(im.resize((1080, H))).astype(float) / 255
        lin = np.where(a <= .04045, a / 12.92, ((a + .055) / 1.055) ** 2.4)
        L = .2126 * lin[..., 0] + .7152 * lin[..., 1] + .0722 * lin[..., 2]
        d = T.get(k, {"tvare": [], "postavy": []})
        hl = [(x - w_ * .35, y - h_ * 1.0, w_ * 1.7, h_ * 2.25) for x, y, w_, h_ in d["tvare"]]
        hl = max(hl, key=lambda r: r[2] * r[3]) if hl else None
        po = max(d["postavy"], key=lambda r: r[2] * r[3]) if d["postavy"] else None
        best = None
        if d["tvare"]:
            x_, y_, w_, h_ = max(d["tvare"], key=lambda r: r[2] * r[3])
            fc, hp = (y_ + h_ / 2) * H, h_ * H
            y = max(0, min(100, round((fc - (50 + 1.5 * hp)) / (H - 720) * 100)))
            top = (H - 720) * y / 100
            if fc + .75 * hp - top < PAS[0] + 20:              # hlava nad pásem textu
                band = L[int(top + PAS[0]):int(top + PAS[1]), 64:1016]
                best = (y, round(1.05 / (np.percentile(band, 92) + .05), 2))
            if best: out.append((k, best[0], best[1], True, bool(po)))
            continue
        for y in range(0, 101, 5):
            top = (H - 720) * y / 100
            if hl:
                hy0, hy1 = hl[1] * H - top, (hl[1] + hl[3]) * H - top
                if hy0 < -10 or hy1 > 730: continue              # hlava celá
                if not (hy1 < PAS[0] + 20 or hy0 > PAS[1] - 20): continue  # hlava mimo pás textu
            if po:
                py0, py1 = po[1] * H - top, (po[1] + po[3]) * H - top
                vid = max(0, min(py1, 720) - max(py0, 0)) / max(1, py1 - py0)
                if vid < .6: continue                            # postava většinou v záběru
            band = L[int(top + PAS[0]):int(top + PAS[1]), 64:1016]
            c = 1.05 / (np.percentile(band, 92) + .05)
            if best is None or c > best[1]: best = (y, round(c, 2))
        if best: out.append((k, best[0], best[1], bool(hl), bool(po)))
out.sort(key=lambda r: -r[2])
for r in out: print(*r)
