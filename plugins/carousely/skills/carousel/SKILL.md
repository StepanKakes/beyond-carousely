---
name: carousel
description: Výroba IG carouselů ve stylech Maddie (VS, karta, Nikdy/Vždycky), Shelby (příběh) a Jeremy (podcast, tweet). Z tvého textu a tvých fotek udělá hotové PNG slidy 1080x1440 s kontrolou čitelnosti. Použij, když chceš carousel, předělat carousel do jiného stylu, roztřídit fotky na carousely, nebo když napíšeš „udělej carousel“, „ve stylu Maddie / Shelby / Jeremy“.
---

# Carousel

Uživatel je klient (typicky Marek Trnka, @marektrnka.sales), ne grafik. Mluv česky, jednoduše, bez technických podrobností. Ptej se jen na to, co opravdu potřebuješ.

## Prostředí

- Plugin: cesta je v `~/.cache/beyond-carousely/plugin_cesta`. Nástroje `$N` = `<plugin>/nastroj`, šablony `<plugin>/sablony`, pravidla `<plugin>/styl.md`.
- Python `$PY`: Mac `~/.cache/beyond-carousely/venv/bin/python3`, Windows `%USERPROFILE%\.cache\beyond-carousely\venv\Scripts\python.exe`.
- Když `plugin_cesta` nebo `$PY` chybí, setup ještě neproběhl: najdi plugin v `~/.claude/plugins/marketplaces/beyond-carousely/plugins/carousely` a spusť `zsh scripts/setup.sh` (Mac) nebo `powershell -ExecutionPolicy Bypass -File scripts\setup.ps1` (Windows). Pak pokračuj.
- Pracovní složka: `~/Documents/carousely/<klient>/` s `fotky/` (banka a `katalog.md`), `avatar.jpg`, `profil.json` (`{"jmeno": "...", "handle": "@..."}`), `texty.md`, JSONy carouselů a `export/`.

**Vždy nejdřív přečti celé `styl.md`.** Je tam šest stylů, jejich principy a pravidla fotek, umístění a typografie.

## Tvrdá pravidla

1. **Obsah je vždy klientův.** Text vezmi od klienta (zadání, `texty.md`) a jen ho rozděl do formátu. Nic nevymýšlej: žádné příběhy, čísla, kariéru, nové příklady. Od tvůrců se bere jen řemeslo (kde hook, kde CTA, kolik textu, rytmus), nikdy jejich témata. Když klient text nemá, napiš ho jeho hlasem z jeho podkladů a nech ho schválit, než renderuješ. Čísla (obrat, roky, počty) jen ta, která klient sám uvedl.
2. **Fotky:** nic se nemaže. Přednost mají zachycené momenty (pracuje, někde je). Ukazující a pózující fotky jen na hook a CTA, a jen když gesto míří na text. Každá fotka v carouselu jednou. Děti jen když klient výslovně chce.
3. **Výřez se řídí postavou:** hlava a hlavní motiv celé, nikdy jen tělo, nohy, strop. Nepřibližuj kvůli textu. Fotky do splitu vybírej ručně podle náhledu.
4. **Čitelnost:** nejdřív výběr fotky a místo textu, pak lehké ztmavení 0,1 až 0,25 (dělá `--kontrola` sama). Ve splitu nikdy černý podklad. Shelby bez stínu.
5. **Split:** text na všech slidech na stejném místě a stejně velký (Maddie `lab_y` 50, Jeremy `lab_y` 92 nahoře i dole). VS začíná rovnou prvním párem vět.
6. **Jazyk:** česky, přirozeně, jak klient mluví. Žádné emoji, pomlčky, šipky, trojice záporů, „Tady je X věcí“. Klíčové slovo CTA bez diakritiky.

## Postup

1. **Klient a složka.** Podívej se do `~/Documents/carousely/`. Když složka klienta existuje, použij ji. Když ne:
   - Marek: jeho připravená složka je ke stažení z Google Drive (odkaz mu poslal Štěpán). Ať ji stáhne a rozbalí do `~/Documents/carousely/`, nebo ti dá cestu k zipu a rozbal ho sám.
   - Nový klient: zeptej se na složku s fotkami, profilovku a IG jméno, pak postav banku (krok 2).
2. **Fotobanka (jen poprvé).** `$PY $N/arch.py <složka> <tmp>/arch 24 6 320`, prohlédni archy, sepiš `seznam.tsv` (`soubor|kategorie|nazev|popis a tip`; kategorie portrety, prace, lifestyle, pribeh, rodina, detaily) a spusť `$PY $N/banka.py <zdroj> <klient>/fotky seznam.tsv`. Profilovku ulož jako `avatar.jpg` celou, neořezávej.
3. **Styl.** Když ho klient neřekl, doporuč jeden podle obsahu a v jedné větě řekni proč:
   - dva přístupy proti sobě (co řekne většina vs co říct): **Maddie VS**
   - text po krocích, hodně textu: **Maddie karta** nebo **Jeremy tweet**
   - konkrétní věty „tohle neříkej / tohle řekni“: **Maddie Nikdy/Vždycky**
   - osobní příběh, lekce, chyba: **Shelby příběh**
   - postup v číslovaných krocích: **Jeremy podcast**
   „Všechny styly“ = udělej všech šest.
4. **JSON.** Zkopíruj `sablony/<styl>.json` do složky klienta, nastav `nazev`, `vystup` (`export/<nazev>`), `jmeno` a `handle` z `profil.json`, a vlož klientův text podle principů stylu ze `styl.md`.
5. **Fotky.** Do splitu: `$PY $N/pulky.py <klient>/fotky [lab_y]` seřadí banku podle klidného místa pro text. Z nejlepších udělej malý náhled půlek, prohlédni ho a vyber. Ostatní formáty podle `katalog.md`.
6. **Render.** `$PY $N/render.py <carousel>.json --kontrola` (jeden slide: přidej jeho číslo). Kontrola posune kartu nebo text a lehce ztmaví, fotku nemění. Řádky POZOR v `export/<nazev>/kontrola.txt` vyřeš jinou fotkou nebo místem textu.
7. **Ověření.** Pošli hotové slidy agentovi `carousely:overovac` a oprav, co najde. Sám se dívej jen na malé náhledy.
8. **Předání.** Ukaž klientovi slidy (cesty k PNG v `export/<nazev>/`, pošli je, pokud to prostředí umí) a jednou větou napiš, co je v carouselu a co by měl zkontrolovat (třeba čísla). Opravy dělej podle jeho slov.
