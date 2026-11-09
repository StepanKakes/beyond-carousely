#!/bin/zsh
# Nastavení pluginu carousely na Macu. Spouští se jednou po instalaci.
set -e
PLUGIN="${0:A:h:h}"
DATA="$HOME/.cache/beyond-carousely"
mkdir -p "$DATA" "$HOME/Documents/carousely"

echo "1/4 Python"
command -v python3 >/dev/null || { echo "Chybí python3. Nainstaluj ho z python.org nebo přes 'xcode-select --install' a spusť setup znovu."; exit 1; }
[ -x "$DATA/venv/bin/python3" ] || python3 -m venv "$DATA/venv"
pipi() { "$DATA/venv/bin/python3" -m pip install --quiet --disable-pip-version-check "$@"; }
# Python z python.org nemá certifikáty, když selže ověření, použij systémové z macOS
pipi pillow numpy pillow-heif 2>/dev/null || SSL_CERT_FILE=/etc/ssl/cert.pem PIP_CERT=/etc/ssl/cert.pem pipi pillow numpy pillow-heif

echo "2/4 Detekce obličejů (Apple Vision)"
if command -v swiftc >/dev/null; then
  swiftc -O "$PLUGIN/nastroj/tvare.swift" -o "$DATA/tvare" 2>/dev/null && echo "   hotovo" || echo "   nešlo přeložit, kontrola pojede bez obličejů"
else
  echo "   chybí swiftc (nainstaluj 'xcode-select --install'), kontrola zatím pojede bez obličejů"
fi

echo "3/4 Prohlížeč"
if [ -d "/Applications/Google Chrome.app" ] || [ -d "/Applications/Microsoft Edge.app" ]; then echo "   nalezen"
else echo "   Chybí Google Chrome. Stáhni ho z google.com/chrome, render ho potřebuje."; fi

echo "4/4 Pracovní složka ~/Documents/carousely"
echo "$PLUGIN" > "$DATA/plugin_cesta"
echo "Hotovo. Restartuj Claude a napiš: /carousely:carousel"
