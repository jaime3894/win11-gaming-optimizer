# Build script: genera Win11GamingOptimizer.exe con PyInstaller
$ErrorActionPreference = "Stop"
$root = $PSScriptRoot
Set-Location $root

Write-Host "==> Instalando PyInstaller (si falta)..." -ForegroundColor Cyan
pip install pyinstaller --quiet --disable-pip-version-check

Write-Host "==> Limpiando builds anteriores..." -ForegroundColor Cyan
Remove-Item -Recurse -Force "$root\build" -ErrorAction SilentlyContinue
Remove-Item -Recurse -Force "$root\dist"  -ErrorAction SilentlyContinue
Remove-Item -Force "$root\Win11GamingOptimizer.spec" -ErrorAction SilentlyContinue

Write-Host "==> Compilando .exe (esto tarda 1-3 minutos)..." -ForegroundColor Cyan
pyinstaller `
    --onefile `
    --windowed `
    --name "Win11GamingOptimizer" `
    --uac-admin `
    --collect-all customtkinter `
    --noconfirm `
    --clean `
    main.py

if ($LASTEXITCODE -ne 0) {
    Write-Host "FALLO en la compilación." -ForegroundColor Red
    exit 1
}

$exe = "$root\dist\Win11GamingOptimizer.exe"
if (Test-Path $exe) {
    $sizeMB = [math]::Round((Get-Item $exe).Length / 1MB, 1)
    Write-Host ""
    Write-Host "==> BUILD OK" -ForegroundColor Green
    Write-Host "    Archivo: $exe"
    Write-Host "    Tamaño:  $sizeMB MB"
    Write-Host ""
    Write-Host "Para distribuirlo: comparte solo Win11GamingOptimizer.exe" -ForegroundColor Yellow
} else {
    Write-Host "FALLO: el .exe no se generó." -ForegroundColor Red
    exit 1
}
