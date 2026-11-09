# Nastavení pluginu carousely na Windows. Spouští se jednou po instalaci.
$ErrorActionPreference = "Stop"
$Plugin = Split-Path -Parent $PSScriptRoot
$Data = Join-Path $HOME ".cache\beyond-carousely"
New-Item -ItemType Directory -Force -Path $Data, (Join-Path $HOME "Documents\carousely") | Out-Null

Write-Host "1/3 Python"
$py = Get-Command python -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command py -ErrorAction SilentlyContinue }
if (-not $py) { Write-Host "Chybí Python. Nainstaluj ho: winget install Python.Python.3.12 a spusť setup znovu."; exit 1 }
$venvPy = Join-Path $Data "venv\Scripts\python.exe"
if (-not (Test-Path $venvPy)) { & $py.Source -m venv (Join-Path $Data "venv") }
& $venvPy -m pip install --quiet --upgrade pip
& $venvPy -m pip install --quiet pillow numpy pillow-heif

Write-Host "2/3 Prohlížeč"
$kand = @("$env:ProgramFiles\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
          "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe", "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe")
if ($kand | Where-Object { Test-Path $_ }) { Write-Host "   nalezen" } else { Write-Host "   Chybí Google Chrome nebo Edge, render ho potřebuje." }

Write-Host "3/3 Pracovní složka Documents\carousely"
Write-Host "   Detekce obličejů je jen na Macu, kontrola tady hlídá čitelnost a hlavy kontroluje agent overovac."
Set-Content -Path (Join-Path $Data "plugin_cesta") -Value $Plugin
Write-Host "Hotovo. Restartuj Claude a napiš: /carousely:carousel"
