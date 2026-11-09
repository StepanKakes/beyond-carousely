#!/usr/bin/env python3
"""Renderer carouselu: JSON se slidy -> PNG 1080x1440 (3:4) přes headless Chrome.

Použití:
  python3 render.py carousel.json [cislo_slidu]            jen vykreslí
  python3 render.py carousel.json --kontrola [cislo_slidu]  ověří čitelnost, případně lehce ztmaví fotku (max 0,25), hlásí text na hlavě

Kontrola: obličeje najde Apple Vision (tvare), text vykreslí zvlášť jako masku a změří kontrast
bílé proti fotce přímo pod písmeny (95. percentil jasu, chytí i světlé nápisy za textem). Když text leží na hlavě nebo je nečitelný,
opravuje v tomhle pořadí: 1. přesun textu (jako Shelby, správný placement), 2. rovnoměrné
ztmavení fotky, 3. černý podklad pod řádky (jako Maddie). Výsledek zapíše zpět do JSON
a do export/.../kontrola.txt.

Formáty slidu (pole "format"), styly popisuje styl.md:
  hook     velký tučný text přes fotku + serifový podtitulek ("varianta": "jeremy")
  pribeh   tučný bílý text jako IG story ("velikost": "maly" / "velky", "zarovnani": "vlevo")
  karta    tmavá karta jako příspěvek na X přes fotku
  tweet    jen příspěvek na X na černém pozadí
  boxy     věty v černých obdélnících, serif
  split    dvě fotky nad sebou, popisky v půlkách, volitelně VS
Společné: "foto", "zoom", "x"/"y" (object-position %), "pozice" (top/mid/bottom/% středu), "tma",
"podklad" (true = černý podklad pod řádky), "stin" ("jemny" / "zadny", jinak bere cfg["stin"]).
Značky v textu: **tučně**, __podtrženě__, ==akcent==, "# " větší řádek, "~ " serif.
"""
import html, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

def najdi_chrome():
    """Chrome nebo Edge na Macu, Windows i Linuxu, případně z proměnné CAROUSELY_CHROME."""
    kand = [os.environ.get("CAROUSELY_CHROME", ""),
            "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
            "/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge"]
    for root in (os.environ.get("PROGRAMFILES", ""), os.environ.get("PROGRAMFILES(X86)", ""), os.environ.get("LOCALAPPDATA", "")):
        if root:
            kand += [os.path.join(root, "Google", "Chrome", "Application", "chrome.exe"),
                     os.path.join(root, "Microsoft", "Edge", "Application", "msedge.exe")]
    kand += [shutil.which(x) or "" for x in ("google-chrome", "chromium", "chromium-browser", "chrome", "msedge")]
    for k in kand:
        if k and os.path.exists(k):
            return k
    sys.exit("Nenašel jsem Google Chrome ani Microsoft Edge. Nainstaluj Chrome a spusť znovu.")


CHROME = najdi_chrome()
DATA = Path.home() / ".cache" / "beyond-carousely"
NASTROJ = os.path.dirname(os.path.abspath(__file__))
W, H = 1080, 1440
PRAH_VELKY, PRAH_MALY = 3.0, 3.8  # kontrast bílé proti pozadí (WCAG ratio)

FONTY = ('<link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800'
         '&family=Montserrat:wght@700;800;900'
         '&family=Source+Serif+4:opsz,wght@8..60,400;8..60,500&display=block" rel="stylesheet">')

CSS = """
*{margin:0;padding:0;box-sizing:border-box}
html,body{width:1080px;height:1440px;overflow:hidden;background:#000}
.s{position:relative;width:1080px;height:1440px;overflow:hidden;font-family:'Plus Jakarta Sans',sans-serif;color:#fff;
  -webkit-font-smoothing:antialiased;text-rendering:geometricPrecision}
.ph{position:absolute;inset:0;overflow:hidden}
.ph img{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}
.tma{position:absolute;inset:0;background:#000}
.stin-jemny .sh{text-shadow:0 1px 10px rgba(0,0,0,.32)}
.red{color:#FFCC00}
.u{text-decoration:underline;text-underline-offset:7px;text-decoration-thickness:3px}
.vrstva{position:absolute;left:0;right:0;display:flex;flex-direction:column;align-items:center;text-align:center}
.hook{font-weight:800;font-size:100px;line-height:1.02;letter-spacing:-.03em;padding:0 64px}
.sub{font-family:'Source Serif 4',Georgia,serif;font-weight:400;font-size:46px;margin-top:16px;letter-spacing:-.005em}
.hook.jeremy{font-family:Montserrat,sans-serif;font-weight:900;font-size:118px;text-transform:uppercase;letter-spacing:-.02em;line-height:.98}
.subj{font-family:Montserrat,sans-serif;font-weight:800;font-size:44px;text-transform:uppercase;color:#FFCC00;margin-top:14px;padding:0 70px;line-height:1.1}
.pr{font-weight:700;font-size:46px;line-height:1.24;letter-spacing:-.01em;padding:0 96px}
.pr.maly{font-size:37px;line-height:1.3;padding:0 130px;letter-spacing:0}
.pr.velky{font-size:56px;line-height:1.16;letter-spacing:-.02em;padding:0 80px}
.pr p+p{margin-top:32px}
.pr .vel{font-size:1.45em;line-height:1.1;letter-spacing:-.02em;font-weight:800}
.pr .serif{font-family:'Source Serif 4',Georgia,serif;font-weight:400;letter-spacing:0}
.vlevo{align-items:flex-start;text-align:left}
.vlevo .pr{padding:0 80px}
.karta{background:#000;border-radius:30px;padding:40px 44px 46px;width:860px;text-align:left;
  box-shadow:0 10px 40px rgba(0,0,0,.25)}
.kh{display:flex;align-items:center;gap:22px;margin-bottom:30px}
.av{width:88px;height:88px;border-radius:50%;object-fit:cover}
.jm{font-weight:700;font-size:31px;line-height:1.15;color:#e7e9ea}
.hd{font-weight:500;font-size:28px;color:#71767b;margin-top:2px}
.dots{margin-left:auto;align-self:flex-start;color:#71767b;font-size:34px;letter-spacing:2px;margin-top:-6px}
.kt{font-weight:500;font-size:31px;line-height:1.38;color:#e7e9ea}
.kt p+p{margin-top:28px}
.tw{position:absolute;left:92px;right:92px;top:50%;transform:translateY(-50%);text-align:left}
.tw .kh{margin-bottom:36px}.tw .av{width:96px;height:96px}
.tw .jm{font-size:34px}.tw .hd{font-size:30px}
.tw .kt{font-size:42px;line-height:1.34}
.tw .kt p+p{margin-top:36px}
.boxy{align-items:center}
.bx{display:inline-block;background:#000;color:#fff;font-family:'Source Serif 4',Georgia,serif;font-weight:400;
  font-size:40px;line-height:1.24;padding:12px 24px 14px;text-align:center;max-width:820px}
.bx.velky{font-size:62px;padding:14px 28px 18px}
.bx+.bx{margin-top:14px}
.pul{position:absolute;left:0;right:0;height:720px;overflow:hidden}
.pul img{width:100%;height:100%;object-fit:cover}
.pul .tma{position:absolute;inset:0}
.pul .pas{position:absolute;left:0;right:0;height:440px;transform:translateY(-50%)}
.uz{margin-left:-.1em}
.grad{position:absolute;left:0;right:0;bottom:0;height:78%;background:linear-gradient(to top,rgba(0,0,0,.84) 0%,rgba(0,0,0,.62) 30%,rgba(0,0,0,.3) 60%,rgba(0,0,0,.08) 85%,rgba(0,0,0,0) 100%)}
.lab{position:absolute;left:0;right:0;text-align:center;font-weight:800;font-size:66px;line-height:1.06;
  letter-spacing:-.025em;padding:0 70px}
.lab.stred{font-size:54px;line-height:1.1}
.lab small{display:block;font-weight:700;font-size:36px;letter-spacing:-.01em;margin-bottom:10px}
.lab .pod{display:block;font-family:'Source Serif 4',Georgia,serif;font-weight:400;font-size:40px;letter-spacing:0;margin-top:12px}
.lab.jer{font-family:Montserrat,sans-serif;font-weight:800;font-size:72px;text-align:left;padding:0 64px;letter-spacing:-.01em}
.lab.jtext{font-weight:700;font-size:36px;line-height:1.36;text-align:left;padding:0 64px;letter-spacing:-.005em}
.lab.jtext p+p{margin-top:26px}
.vs{position:absolute;left:0;right:0;top:720px;transform:translateY(-58%);text-align:center;font-weight:800;
  font-size:84px;letter-spacing:-.02em}
.hl{background:#000;padding:.06em .28em .1em;-webkit-box-decoration-break:clone;box-decoration-break:clone;line-height:1.5}
"""

CSS_FOTO = ".vrstva:not(.boxy),.lab,.vs{visibility:hidden!important}"
CSS_MASKA = """
.ph,.pul,.tma,.grad,.pas{visibility:hidden!important}
body,.s{background:#000!important}
*{text-shadow:none!important}
.red,.u{color:inherit!important}
.sub,.subj,.pr p,.lab small,.lab .pod,.lab.jtext,.lab.jtext p{color:#0f0!important}
.hook,.hook *,.lab,.vs,.pr p.vel,.pr.velky p,.lab.jer *{color:#f00!important}
.lab small{color:#0f0!important}
.karta *,.tw *,.bx *{visibility:hidden!important}
.karta,.bx{background:#00f!important;color:transparent!important;box-shadow:none!important}
.hl{background:transparent!important}
"""


def md(t):
    t = html.escape(t)
    # česká typografie: jednopísmenné předložky a spojky k dalšímu slovu, poslední slovo nezůstane samo
    t = re.sub(r"(?<![\w&])([vkszaiouVKSZAIOU]) ", "\\1\u00a0", t)
    t = "\n".join(re.sub(r" (\S{1,14})$", "\u00a0\\1", r) if len(r) > 24 else r for r in t.split("\n"))
    t = re.sub(r"(\w+-\w+)", r'<span style="white-space:nowrap">\1</span>', t)
    t = re.sub(r"\*\*(.+?)\*\*", r"<b>\1</b>", t)
    t = re.sub(r"__(.+?)__", r'<span class="u">\1</span>', t)
    t = re.sub(r"==(.+?)==", r'<span class="red">\1</span>', t)
    t = t.replace("“", '<span class="uz">“</span>')
    return t.replace("\n", "<br>")


def hl(t, ano):
    return f'<span class="hl">{t}</span>' if ano else t


def img_tag(path, s):
    zoom = s.get("zoom", 1)
    x, y = s.get("x", 50), s.get("y", 50)
    st = f"object-position:{x}% {y}%;transform:scale({zoom});transform-origin:{x}% {y}%"
    return f'<img src="{Path(path).as_uri()}" style="{st}">'


def poz(v, default):
    v = v if v is not None else default
    if v == "top": return "top:96px"
    if v == "bottom": return "bottom:120px"
    if v == "mid": return "top:50%;transform:translateY(-50%)"
    return f"top:{v}%;transform:translateY(-50%)"


def odstavce(items, box):
    out = []
    for p in items:
        cls = ""
        if p.startswith("# "): cls, p = "vel", p[2:]
        elif p.startswith("~ "): cls, p = "serif", p[2:]
        out.append(f'<p class="{cls}">{hl(md(p), box)}</p>')
    return "".join(out)


def hlavicka(cfg):
    return (f'<div class="kh"><img class="av" src="{Path(cfg["avatar"]).as_uri()}">'
            f'<div><div class="jm">{html.escape(cfg["jmeno"])}</div><div class="hd">{html.escape(cfg["handle"])}</div></div>'
            f'<div class="dots">···</div></div>')


def slide_html(s, cfg, mode="normal"):
    f = lambda p: os.path.join(cfg["fotky"], p)
    out = []
    fmt = s["format"]
    box = bool(s.get("podklad"))
    if fmt in ("hook", "pribeh", "karta", "boxy"):
        out.append(f'<div class="ph">{img_tag(f(s["foto"]), s)}</div>')
        if s.get("tma"):
            out.append(f'<div class="tma" style="opacity:{s["tma"]}"></div>')
        if s.get("grad"):
            out.append('<div class="grad" style="height:55%"></div>')
    if fmt == "hook":
        if s.get("varianta") == "jeremy":
            sub = f'<div class="subj sh">{hl(md(s["sub"]), box)}</div>' if s.get("sub") else ""
            out.append(f'<div class="vrstva" style="{poz(s.get("pozice"), 62)}"><div class="hook jeremy sh">{hl(md(s["text"]), box)}</div>{sub}</div>')
        else:
            sub = f'<div class="sub sh">{hl(md(s["sub"]), box)}</div>' if s.get("sub") else ""
            out.append(f'<div class="vrstva" style="{poz(s.get("pozice"), "mid")}"><div class="hook sh">{hl(md(s["text"]), box)}</div>{sub}</div>')
    elif fmt == "pribeh":
        vl = " vlevo" if s.get("zarovnani") == "vlevo" else ""
        out.append(f'<div class="vrstva{vl}" style="{poz(s.get("pozice"), "mid")}"><div class="pr {s.get("velikost", "")} sh">{odstavce(s["text"], box)}</div></div>')
    elif fmt == "karta":
        ps = "".join(f"<p>{md(p)}</p>" for p in s["text"])
        out.append(f'<div class="vrstva" style="{poz(s.get("pozice"), "top")}"><div class="karta">{hlavicka(cfg)}<div class="kt">{ps}</div></div></div>')
    elif fmt == "tweet":
        ps = "".join(f"<p>{md(p)}</p>" for p in s["text"])
        out.append(f'<div class="tw">{hlavicka(cfg)}<div class="kt">{ps}</div></div>')
    elif fmt == "boxy":
        bs = "".join(f'<div class="bx{" velky" if b.startswith("# ") else ""}">{md(b[2:] if b.startswith("# ") else b)}</div>' for b in s["text"])
        out.append(f'<div class="vrstva boxy" style="{poz(s.get("pozice"), "mid")}">{bs}</div>')
    elif fmt == "split":
        for part, top in (("horni", 0), ("dolni", 720)):
            p = s[part]
            pb = bool(p.get("podklad", box))
            g = '<div class="grad"></div>' if p.get("grad") else ""
            t = f'<div class="tma" style="opacity:{p["tma"]}"></div>' if p.get("tma") else ""
            ly = p.get("lab_y", 62)
            # měkké ztmavení jen za textem (bílý stůl za postavou), žádný ostrý podklad
            ps = p.get("pas")
            ps = (f'<div class="pas" style="top:{720 * ly / 100}px;background:linear-gradient(to bottom,rgba(0,0,0,0),'
                  f'rgba(0,0,0,{ps}) 32%,rgba(0,0,0,{ps}) 68%,rgba(0,0,0,0))"></div>') if ps else ""
            out.append(f'<div class="pul" style="top:{top}px">{img_tag(f(p["foto"]), p)}{t}{ps}{g}</div>')
            styl = p.get("styl", "")
            if isinstance(p.get("text"), list):
                obsah = "".join(f"<p>{hl(md(t), pb)}</p>" for t in p["text"])
            else:
                maly = f'<small>{hl(md(p["maly"]), pb)}</small>' if p.get("maly") else ""
                pod = f'<span class="pod">{hl(md(p["pod"]), pb)}</span>' if p.get("pod") else ""
                obsah = f'{maly}{hl(md(p["text"]), pb)}{pod}'
            # Jeremy: blok přichycený spodní hranou, ať nadpis i vysvětlení stojí vždy na stejném místě bez ohledu na počet řádků
            posun = "-100%" if styl in ("jer", "jtext") else "-50%"
            out.append(f'<div class="lab {styl} sh" style="top:{top + 720 * ly / 100}px;transform:translateY({posun})">{obsah}</div>')
        if s.get("vs", True):
            out.append('<div class="vs sh">VS</div>')
    stin = s.get("stin", cfg.get("stin", "jemny"))
    extra = {"normal": "", "foto": CSS_FOTO, "maska": CSS_MASKA}[mode]
    return (f'<!doctype html><html><head><meta charset="utf-8">{FONTY}<style>{CSS}{extra}</style></head>'
            f'<body><div class="s stin-{stin}">{"".join(out)}</div></body></html>')


def chrome(html_text, png, tmp):
    hp = png + ".html"
    open(hp, "w", encoding="utf-8").write(html_text)
    for _ in range(3):
        try:
          r = subprocess.run([CHROME, "--headless=new", "--disable-gpu", "--hide-scrollbars", "--allow-file-access-from-files",
                            f"--user-data-dir={os.path.join(tmp, 'profil')}", f"--window-size={W},{H}",
                            "--virtual-time-budget=6000", "--force-device-scale-factor=1",
                            f"--screenshot={png}", Path(hp).resolve().as_uri()], capture_output=True, timeout=90)
        except subprocess.TimeoutExpired:
            continue
        if r.returncode == 0:
            os.remove(hp)
            return png
    sys.exit(f"Chrome selhal: {png}")


# ---------- kontrola ----------

_tvare = {}


def tvar_bin():
    for k in (os.environ.get("CAROUSELY_TVARE", ""), str(DATA / "tvare"), os.path.join(NASTROJ, "tvare")):
        if k and os.path.exists(k):
            return k
    return None


def najdi_tvare(cesty):
    """Obličeje přes Apple Vision (jen Mac). Bez něj vrátí jen rozměry a kontrola hlídá jen čitelnost."""
    b = tvar_bin()
    if b:
        return json.loads(subprocess.run([b] + cesty, capture_output=True, text=True, check=True).stdout)
    from PIL import Image, ImageOps
    out = {}
    for c in cesty:
        w, h = ImageOps.exif_transpose(Image.open(c)).size
        out[c] = {"w": w, "h": h, "tvare": [], "postavy": [], "bez_detekce": True}
    return out


def tvare(cfg, foto):
    """Normalizované obdélníky hlav (obličej rozšířený o vlasy a bradu)."""
    cesta = os.path.join(cfg["fotky"], foto)
    if cesta not in _tvare:
        cache = os.path.join(cfg["fotky"], ".tvare.json")
        data = json.load(open(cache, encoding="utf-8")) if os.path.exists(cache) else {}
        if foto not in data:
            data[foto] = najdi_tvare([cesta])[cesta]
            json.dump(data, open(cache, "w", encoding="utf-8"), indent=1)
        _tvare[cesta] = data[foto]
    d = _tvare[cesta]
    hlavy = []
    for x, y, w, h in d["tvare"]:
        # obličej + vlasy a temeno nad ním + brada
        hlavy.append([x - w * .35, y - h * 1.0, w * 1.7, h * 2.25])
    for x, y, w, h in d.get("postavy", []):
        # postava bez nalezeného obličeje (zády, sklopená hlava): hlava = horní třetina horní poloviny těla
        if not any(x <= fx + fw / 2 <= x + w and y <= fy + fh / 2 <= y + h for fx, fy, fw, fh in d["tvare"]):
            hlavy.append([x + w * .2, y - h * .05, w * .6, h * .4])
    return d["w"], d["h"], hlavy


def na_slide(rects, iw, ih, s, box):
    """Normalizované obdélníky fotky -> pixely slidu (object-fit cover, object-position, zoom)."""
    bx, by, bw, bh = box
    x, y, z = s.get("x", 50), s.get("y", 50), s.get("zoom", 1)
    k = max(bw / iw, bh / ih)
    dw, dh = iw * k, ih * k
    ox, oy = bx + (bw - dw) * x / 100, by + (bh - dh) * y / 100
    cx, cy = bx + bw * x / 100, by + bh * y / 100
    out = []
    for u, v, w, h in rects:
        x0, y0 = ox + u * dw, oy + v * dh
        x1, y1 = x0 + w * dw, y0 + h * dh
        x0, x1 = cx + (x0 - cx) * z, cx + (x1 - cx) * z
        y0, y1 = cy + (y0 - cy) * z, cy + (y1 - cy) * z
        x0, y0, x1, y1 = max(x0, bx), max(y0, by), min(x1, bx + bw), min(y1, by + bh)
        if x1 > x0 and y1 > y0:
            out.append((int(x0), int(y0), int(x1), int(y1)))
    return out


def hlavy_slidu(s, cfg):
    if s["format"] == "tweet":
        return []
    if s["format"] == "split":
        r = []
        for part, top in (("horni", 0), ("dolni", 720)):
            iw, ih, hl_ = tvare(cfg, s[part]["foto"])
            r += na_slide(hl_, iw, ih, s[part], (0, top, W, 720))
        return r
    iw, ih, hl_ = tvare(cfg, s["foto"])
    return na_slide(hl_, iw, ih, s, (0, 0, W, H))


def hlava_cela(s_part, cfg, box):
    """True, když je největší hlava na fotce v záběru (aspoň 90 % plochy). Bez obličeje vždy True."""
    iw, ih, hl_ = tvare(cfg, s_part["foto"])
    if not hl_:
        return True
    u, v, w, h = max(hl_, key=lambda r: r[2] * r[3])
    bx, by, bw, bh = box
    x, y, z = s_part.get("x", 50), s_part.get("y", 50), s_part.get("zoom", 1)
    k = max(bw / iw, bh / ih)
    dw, dh = iw * k, ih * k
    ox, oy = bx + (bw - dw) * x / 100, by + (bh - dh) * y / 100
    cx, cy = bx + bw * x / 100, by + bh * y / 100
    x0, y0 = cx + (ox + u * dw - cx) * z, cy + (oy + v * dh - cy) * z
    x1, y1 = cx + (ox + (u + w) * dw - cx) * z, cy + (oy + (v + h) * dh - cy) * z
    cela = (x1 - x0) * (y1 - y0)
    vid = max(0, min(x1, bx + bw) - max(x0, bx)) * max(0, min(y1, by + bh) - max(y0, by))
    return cela > 0 and vid / cela >= .9


def zmer(foto_png, maska_png, hlavy, oblast=(0, 0, W, H)):
    """Vrátí (kontrast velkého, kontrast malého, překryv hlavy v px)."""
    import numpy as np
    from PIL import Image, ImageFilter
    x0, y0, x1, y1 = oblast
    m = np.asarray(Image.open(maska_png).convert("RGB")).astype(int)[y0:y1, x0:x1]
    f = np.asarray(Image.open(foto_png).convert("RGB")).astype(float)[y0:y1, x0:x1] / 255
    lin = np.where(f <= .04045, f / 12.92, ((f + .055) / 1.055) ** 2.4)
    L = .2126 * lin[..., 0] + .7152 * lin[..., 1] + .0722 * lin[..., 2]
    R, G, B = m[..., 0], m[..., 1], m[..., 2]
    vysledek = []
    for sel in ((R > 128) & (G < 100) & (B < 100), (G > 128) & (R < 100)):
        if sel.sum() < 30:
            vysledek.append(None)
            continue
        dil = np.asarray(Image.fromarray((sel * 255).astype("uint8")).filter(ImageFilter.MaxFilter(9))) > 0
        lb = np.percentile(L[dil], 95)
        vysledek.append(round(1.05 / (lb + .05), 2))
    obsazeno = (R > 128) | (G > 128) | (B > 128)
    prekryv = 0
    for hx0, hy0, hx1, hy1 in hlavy:
        a, b = max(hx0, x0) - x0, max(hy0, y0) - y0
        c, d = min(hx1, x1) - x0, min(hy1, y1) - y0
        if c > a and d > b:
            prekryv += int(obsazeno[b:d, a:c].sum())
    return vysledek[0], vysledek[1], prekryv


TMA_KROKY = (0, .1, .15, .2, .25)
PAS_KROKY = (.2, .3, .4)   # měkký pás za textem ve splitu, když plošné ztmavení nestačí
TMA_MAX = TMA_KROKY[-1]


def projde(m):
    v, mal, prek = m
    ok_v = v is None or v >= PRAH_VELKY
    ok_m = mal is None or mal >= PRAH_MALY
    return ok_v and ok_m and prek == 0


def skore(m):
    v, mal, _ = m
    return min(v if v is not None else 99, (mal if mal is not None else 99) * PRAH_VELKY / PRAH_MALY)


def kontrola_slidu(i, s, cfg, tmp):
    """Fotky se nikdy neořezávají, nepřibližují ani nevyměňují. Když text není čitelný,
    fotka se jen rovnoměrně lehce ztmaví (nejvýš TMA_MAX). Překryv hlavy se jen hlásí."""
    fmt = s["format"]
    if fmt == "tweet":
        return f"{i:02d} tweet: bez fotky, OK"
    cache = {}

    def mer(s2, oblasti):
        key = json.dumps(s2, sort_keys=True)
        if key not in cache:
            fp = chrome(slide_html(s2, cfg, "foto"), os.path.join(tmp, f"k{i}_{len(cache)}_f.png"), tmp)
            mp = chrome(slide_html(s2, cfg, "maska"), os.path.join(tmp, f"k{i}_{len(cache)}_m.png"), tmp)
            cache[key] = [zmer(fp, mp, hlavy_slidu(s2, cfg), o) for o in oblasti]
        return cache[key]

    def cte(m):
        v, mal, _ = m
        return (v is None or v >= PRAH_VELKY) and (mal is None or mal >= PRAH_MALY)

    POZICE = ["top", 22, 32, 44, 56, 68, "bottom"]
    if fmt in ("karta", "boxy"):
        # karta se smí jen posunout nahoru nebo dolů, fotka zůstává
        for p in [s.get("pozice")] + [x for x in (["top", "bottom"] if fmt == "karta" else POZICE) if x != s.get("pozice")]:
            s2 = dict(s, pozice=p) if p is not None else dict(s)
            if mer(s2, [(0, 0, W, H)])[0][2] == 0:
                if p is not None: s["pozice"] = p
                return f"{i:02d} {fmt}: pozice {p}, hlava volná"
        return f"{i:02d} {fmt}: POZOR, karta/boxy leží na hlavě ve všech pozicích, vyber jinou fotku"

    if fmt in ("hook", "pribeh"):
        # nejdřív umístění textu, pak lehké ztmavení; fotka zůstává
        nejlepsi = None
        for p in [s.get("pozice")] + [x for x in POZICE if x != s.get("pozice")]:
            for tma in TMA_KROKY:
                s2 = dict(s, tma=tma)
                if p is not None: s2["pozice"] = p
                m = mer(s2, [(0, 0, W, H)])[0]
                if m[2]: break
                if cte(m):
                    if p is not None: s["pozice"] = p
                    if tma: s["tma"] = tma
                    else: s.pop("tma", None)
                    return f"{i:02d} {fmt}: pozice {p}, tma {tma}, kontrast {m[0]}/{m[1]}"
                if nejlepsi is None or skore(m) > skore(nejlepsi[2]): nejlepsi = (p, tma, m)
        p, tma, m = nejlepsi
        if p is not None: s["pozice"] = p
        s["tma"] = tma
        return f"{i:02d} {fmt}: pozice {p}, tma {tma}, kontrast {m[0]}/{m[1]}, POZOR nečitelné, vyber jinou fotku"

    if fmt == "split":
        casti = [("horni", s["horni"], (0, 0, W, 720), 0), ("dolni", s["dolni"], (0, 720, W, H), 1)]
    else:
        casti = [("slide", s, (0, 0, W, H), 0)]
    zpravy = []
    for nazev, cil, oblast, idx in casti:
        vysl = None
        cil.pop("pas", None)
        # nejdřív plošné lehké ztmavení, u splitu pak navíc měkký pás za textem
        kroky = [(t_, 0) for t_ in TMA_KROKY] + ([(TMA_KROKY[-1], p_) for p_ in PAS_KROKY] if fmt == "split" else [])
        for tma, pas in kroky:
            s2 = json.loads(json.dumps(s))
            c2 = s2[nazev] if fmt == "split" else s2
            c2["tma"] = tma
            if pas: c2["pas"] = pas
            m = mer(s2, [(0, 0, W, 720), (0, 720, W, H)] if fmt == "split" else [oblast])[idx]
            vysl = (tma, pas, m)
            if cte(m):
                break
        tma, pas, m = vysl
        if tma: cil["tma"] = tma
        else: cil.pop("tma", None)
        if pas: cil["pas"] = pas
        t = f"{nazev}: tma {tma}{f', pas {pas}' if pas else ''}, kontrast {m[0]}/{m[1]}"
        if not cte(m): t += ", POZOR nečitelné i po ztmavení, vyber jinou fotku nebo místo textu"
        if m[2]: t += ", POZOR text na hlavě"
        zpravy.append(t)
    return f"{i:02d} {fmt}: " + "; ".join(zpravy)


def main():
    args = sys.argv[1:]
    kontrola = "--kontrola" in args
    args = [a for a in args if a != "--kontrola"]
    cfg_path = args[0]
    cfg = json.load(open(cfg_path, encoding="utf-8"))
    base = os.path.dirname(os.path.abspath(cfg_path))
    cfg_abs = dict(cfg)
    cfg_abs["fotky"] = os.path.normpath(os.path.join(base, cfg["fotky"]))
    cfg_abs["avatar"] = os.path.normpath(os.path.join(base, cfg["avatar"]))
    outdir = os.path.join(base, cfg.get("vystup", "export"))
    os.makedirs(outdir, exist_ok=True)
    jen = int(args[1]) if len(args) > 1 else None
    tmp = tempfile.mkdtemp()
    report = []
    for i, s in enumerate(cfg["slidy"], 1):
        if jen and i != jen: continue
        if kontrola:
            radek = kontrola_slidu(i, s, cfg_abs, tmp)
            report.append(radek)
            print(radek)
        png = chrome(slide_html(s, cfg_abs), os.path.join(outdir, f"{i:02d}.png"), tmp)
        if not kontrola: print(png)
    if kontrola:
        json.dump(cfg, open(cfg_path, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        open(os.path.join(outdir, "kontrola.txt"), "w", encoding="utf-8").write("\n".join(report) + "\n")


if __name__ == "__main__":
    main()
