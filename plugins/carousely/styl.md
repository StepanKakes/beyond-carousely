# Styly carouselů

Postup výroby je ve skillu `carousel` tohoto pluginu.

Šablona každého stylu je v `sablony/<styl>.json` (ukázka na tématu Námitky #1 od Marka Trnky). Nový carousel začíná kopií šablony do složky klienta.

## Proč fungují (společné)

1. Vypadají jako běžný příspěvek člověka, ne jako navržená reklama: text jako IG story nebo screenshot z X, žádné šablony, rámečky ani gradientové pásy (kromě Jeremyho podcastu).
2. Fotky jsou skutečný život: práce v terénu, cesty, auto, hotel, letiště. Vypadá to, že ho někdo vyfotil, když někde byl nebo pracoval.
3. Slide 1 hned ukáže formát (split, karta, číslo), žádná titulní karta s vysvětlováním.
4. Jedna šablona se opakuje, mění se text a fotka. Rytmus nutí swipovat.
5. Jedna myšlenka na slide, krátké věty.
6. Kdo jsem s čísly + CTA „napiš do komentáře X“.

## Šest stylů

### Maddie (maddiesells), tři typy, často split

**M1 VS citáty**, šablona `sablony/maddie-vs.json`
- Dvě různé fotky nad sebou, uprostřed velké VS. V každé půlce nahoře tučná bílá věta v uvozovkách (66 px), pod ní malý serif (kdo to říká).
- Hodí se, když má klientův text dva přístupy proti sobě (co řekne většina vs co říct).
- Fotky: obě půlky z běžného dne, osoba ve spodní části půlky (text je nahoře). Půlky k sobě nemusí patřit místem.
- Na konci jeden celý slide „Proč na tom záleží?“ (tučně + serif) a kdo jsem jako bílý text vlevo přes fotku z akce.

**M2 karta**, šablona `sablony/maddie-karta.json`
- Černá karta jako příspěvek na X (avatar = celá profilovka bez ořezu, jméno, @handle, tři tečky) nahoře, fotka přes celý slide.
- Hodí se na jakýkoli text po krocích. Nejlíp se čte a nejvíc textu unese.
- Fotky: každý slide jiné místo, osoba v dolní polovině. CTA: fotka, kde ukazuje nahoru na kartu.

**M3 Nikdy neříkej / Vždycky řekni**, šablona `sablony/maddie-nikdy-vzdy.json`
- Dvě fotky nad sebou ze STEJNÉHO místa a oblečení (série z focení), bez VS. Jedna krátká tučná věta uprostřed každé půlky.
- Hodí se, když má klientův text konkrétní věty „tohle neříkej / tohle řekni“. Pak kdo jsem a závěr v černých boxech se serifem.
- Fotky: série, kde se mění jen moment (veletrh u notebooku, Dubaj nahoře, studio s kamerou).

### Shelby (Shelby Sapp), jeden typ

**S příběh**, šablona `sablony/shelby-pribeh.json`
- Malý tučný bílý text uprostřed nahoře jako v IG story (37 px), jen stín, žádné pozadí. Každý slide jiná aspirační fotka.
- Hook spojí klientův důkaz a zvědavost z jeho vlastního textu.
- Hodí se na osobní lekce, názory, příběhy. Fotky skoro bez obličeje: krajina, bazén, hotel, auto zezadu, letadlo, detail ruky. Text vždy v obloze nebo na klidné ploše.

### Jeremy (Jeremy Lee Miner), dva typy, akcent #FFCC00

**J1 podcast čísla**, šablona `sablony/jeremy-podcast.json`
- Hook: obří verzálky Montserrat Black („5 VĚT“) + žlutý podtitulek, přes fotku ze studia s tmavým přechodem dole.
- Každý slide split dvou záběrů ze stejného studia: nahoře „1. ==Slovo==“ (číslo bílé, slovo žluté) na spodku půlky, dole vysvětlení vlevo přes tmavý přechod.
- Hodí se, když jde klientův text rozdělit do číslovaných kroků. Fotky: studiové a podcastové záběry (u stolu, mikrofon, kamera v popředí), dva různé momenty na slide.

**J2 tweet**, šablona `sablony/jeremy-tweet.json`
- Jen příspěvek na X na černém pozadí, bez fotky. Číslovaný bod, pak „Neříkej: … / Řekni: …“, další slide „Krátké vysvětlení:“.
- Nejrychlejší výroba, hodí se na jakýkoli čistě textový obsah. Klientův text 1:1, jeden krok na příspěvek, bez emoji.

## Struktura: principy tvůrců, ne jejich obsah

**Obsah je vždy klientův.** Sdělení, věty a čísla se berou z klientova textu (`texty.md` ve složce klienta). Od tvůrců se bere jen řemeslo: kde je hook, kde CTA a představení, kolik textu unese slide, jak se opakuje šablona. Témata z inspirace (hovor vs mail vs schůzka, 5 vět, slova Cena/Investice) jsou jen jeden z mnoha jejich obsahů, nikdy šablona. Nic nepřidávat (vymyšlené příběhy, čísla, kariéru), jen rozdělit klientův text do formátu. Když se věta do formátu nevejde, rozdělit ji, ne přepsat.

| styl | hook | představení a důkaz | text na slide | rytmus | CTA |
|---|---|---|---|---|---|
| M1 VS | žádný, slide 1 je rovnou první pár | až na konci, když divák dostal hodnotu | jedna věta na půlku, max 3 řádky | páry „jak to dělá většina“ vs „jak to dělat“, pak jeden slide proč | poslední slide, samostatně |
| M2 karta | karta s jednou větou, která slibuje nebo provokuje | kdekoli jako jedna karta, typicky druhá nebo poslední | nejvíc, 2 až 4 krátké odstavce | jedna karta = jeden krok sdělení | spojené se závěrem v poslední kartě, fotka ukazuje na kartu |
| M3 Nikdy/Vždycky | žádný, slide 1 je první pár | boxy po párech | jedna krátká věta na půlku | páry „nedělej / dělej“, pak boxy | poslední box nebo popisek |
| Shelby | výsledek nebo důkaz + zvědavost v jedné větě, končí třemi tečkami | v hooku, jinde ne | 1 až 3 krátké řádky | jedna myšlenka na slide, gradace | poslední slide, osobní |
| J1 podcast | obří krátké heslo + žlutý podtitulek | žádné nebo jen v CTA | nadpis 1 až 3 slova, pod tím 1 až 2 věty | číslované kroky | poslední slide s magnetem |
| J2 tweet | jedna věta, sama na slidu | volné | 1 až 4 krátké řádky, víc vzduchu než textu | jeden krok sdělení na příspěvek | poslední příspěvek, závěr + CTA |

**Struktura sdělení** (hook, kontext, oddálení, hodnota, hodnota, CTA): kroky sdělení zůstávají všechny, styl jen určuje, kam se který dá. Karta a tweet je mají 1:1 v pořadí. U VS a Nikdy/Vždycky je oddálení strana „průměrný obchodník“ a kontext jde na konec. U Shelby je kontext v hooku. U Jeremyho podcastu je kontext v CTA.

## Fotky

- Fotobanka klienta je roztříděná podle obsahu (`fotky/katalog.md`), nic se nemaže.
- Přednost mají fotky, kde to vypadá, že ho někdo zachytil, když někde je nebo pracuje: veletrh, jednání, notebook, auto, cesty, studio při natáčení.
- Ukazující a pózující fotky jen na hook a CTA, a jen když gesto míří na text. Ve splitech a hodnotových slidech nikdy.
- Splity: M3 a J1 dvojice ze stejného místa, M1 dvě různé scény.
- Každý slide jiná fotka, v jednom carouselu žádná dvakrát.
- Fotky s dětmi jen se souhlasem klienta.

## Umístění (nic nepřekrýt, nic zbytečně neuseknout)

- Formát 1080×1440 (3:4), iPhone fotky se vejdou skoro celé.
- Text nikdy přes obličej. Když je obličej vysoko a text nahoře: `zoom` 1.2 až 1.35 s `y: 0` (zvětšuje se od horní hrany a obličej sjede dolů). Jinak text dolů (`pozice: bottom`).
- Split je čistý: text vždy uprostřed půlky (`lab_y` 50); u Jeremyho pevně přichycený spodní hranou, nadpis těsně nad středem slidu (`lab_y` 92), vysvětlení dole (`lab_y` 92), nikdy se nepřesouvá, stejné místo a velikost na všech slidech, nikdy černý podklad. Čitelnost se řeší jen výběrem fotky a výřezem (`y`, `zoom`), případně mírným ztmavením. Půlka ukazuje 50 % výšky fotky, start výřezu = y/2 % výšky. Hlava musí být v půlce celá (kontrola pustí jen výřez s aspoň 90 % hlavy), nikdy samotné tělo, nohy nebo rozkrok. Obličej musí být nad nebo pod středem půlky. Rušné pozadí za středem (nápisy, stánky, lidé) = jiná fotka. Věty max na tři řádky, delší rozdělit do dvou slidů.
- Fotky do splitu vybírat ručně podle náhledu půlky (skript `nastroj/pulky.py` seřadí banku podle klidného místa pro text). Půlka ukáže jen polovinu výšky fotky na výšku, takže výřez se řídí postavou: hlava a hlavní motiv celé, bez přiblížení. Denní světlé fotky z veletrhu se na bílý text uprostřed nehodí, lepší jsou tmavé záběry ze studia, večerní ulice, výhledy. Automatika fotky nikdy nemění ani neořezává. Když text není čitelný, jen rovnoměrně lehce ztmaví fotku (0,1 až 0,25, schválil Štěpán 8.11.2026). Když nestačí ani to, nahlásí POZOR a fotku vybírám znovu.
- Čitelnost řeší hlavně umístění (Shelby nepoužívá žádný stín, text dává jen do oblohy nebo na tmavou plochu). Stín jen jemný a ne u Shelby. Když umístění nestačí: rovnoměrné ztmavení fotky, u příběhových slidů nakonec černý podklad pod řádky jako Maddie (u splitů nikdy).
- Vždy renderovat s `--kontrola`: Apple Vision najde obličeje, maska textu se změří proti fotce (prahy kontrastu 3,0 velký text, 3,8 malý), text na hlavě nebo nečitelný se automaticky přesune, ztmaví nebo podloží. Report `kontrola.txt` v exportu, POZOR řádky řešit ručně jinou fotkou.
- Pak kontaktní arch a projít ořez gest a celkový dojem.

## Text a jazyk

- Česky, přirozeně, jak klient mluví (třeba kšeft, dobrý, jasný, blbec). Žádné doslovné překlady.
- Bez AI slopu: žádné trojice zápor, žádné „Tady je X věcí“, žádné emoji, šipky ani pomlčky.
- Klíčové slovo CTA bez diakritiky (NAMITKA), podtržené nebo v akcentové barvě.
- Čísla v kontextu musí být klientova vlastní.

## Typografie

- Základní text všude Plus Jakarta Sans (nejblíž Instagram Sans), i v kartách a tweetech. U Maddie větší (citáty 66 px, hook 100 px). Serif Source Serif 4.
- Karta a tweet: jméno #e7e9ea, handle #71767b.
- Jeremy: nadpisy a čísla Montserrat 800 až 900, akcent #FFCC00, text Plus Jakarta Sans.
- Stín textu jen jemný `0 1px 10px rgba(0,0,0,.32)`, u Shelby žádný (`"stin": "zadny"`).

## Výroba

`$PY` je Python pluginu, `$N` složka `nastroj` pluginu, viz skill.

```
$PY $N/render.py <carousel>.json [--kontrola] [cislo_slidu]
$PY $N/pulky.py <klient>/fotky [lab_y]      # pořadí fotek pro split
$PY $N/banka.py <zdroj> <klient>/fotky seznam.tsv
$PY $N/arch.py <složka> <výstup> 24 6 320    # kontaktní archy
```
Formáty: `hook` (varianta `jeremy`), `pribeh` (`velikost` maly/velky, `zarovnani` vlevo), `karta`, `tweet`, `boxy`, `split` (půlky `horni`/`dolni`: `text` nebo seznam, `maly`, `pod`, `lab_y`, `styl` stred/jer/jtext, `grad`; `vs`). Značky: `**tučně**`, `__podtrženě__`, `==akcent==`, `# ` větší řádek, `~ ` serif.
