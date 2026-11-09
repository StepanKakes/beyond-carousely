# Carousely od Beyond

Plugin do Claude, který z tvého textu a tvých fotek udělá hotové IG carousely v šesti osvědčených stylech. Hlídá, aby byl text čitelný, nešel přes obličej a fotky nebyly zbytečně useknuté.

## Instalace

Potřebuješ aplikaci **Claude** (záložka Code) nebo Claude Code a **Google Chrome**. Funguje na Macu i Windows, GitHub účet nepotřebuješ.

Vlož do Claude tenhle jeden prompt:

```
Nainstaluj mi plugin Carousely od Beyond. Spusť `claude plugin marketplace add StepanKakes/beyond-carousely` a `claude plugin install carousely@beyond-carousely`. Pak spusť jeho setup: na Macu `zsh ~/.claude/plugins/marketplaces/beyond-carousely/plugins/carousely/scripts/setup.sh`, na Windows `powershell -ExecutionPolicy Bypass -File "$HOME\.claude\plugins\marketplaces\beyond-carousely\plugins\carousely\scripts\setup.ps1"`. Když něco chybí (Python, Chrome), řekni mi jednoduše, co mám udělat. Na konci mi napiš, ať restartuju Claude.
```

Pak Claude restartuj. Hotovo.

Své fotky dostaneš jako zip, rozbal ho do složky `Dokumenty/carousely`. Když fotky ještě roztříděné nemáš, Claude to udělá s tebou při prvním carouselu.

## Jak se to používá

Napiš Claudovi, co chceš. Například:

- „Udělej carousel na námitku Pošlete mi to mailem ve stylu Maddie karta.“
- „Tady je můj text, udělej z něj carousel. Styl vyber sám.“
- „Udělej Námitky #3 ve všech šesti stylech, ať si vyberu.“
- „Slide 3 je nečitelný, dej tam jinou fotku.“

Nebo napiš `/carousely:carousel` a za to zadání.

Hotové slidy najdeš v `Dokumenty/carousely/<tvoje složka>/export/`.

Styly a kdy který použít: [docs/STYLY.md](docs/STYLY.md).
