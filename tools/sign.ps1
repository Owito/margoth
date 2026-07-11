<#
.SYNOPSIS
    Firma (Authenticode) el ejecutable de Margoth y/o el instalador.

.DESCRIPTION
    Usa el certificado de firma de código del almacén del usuario
    (Cert:\CurrentUser\My) sin necesidad de signtool ni de la contraseña del
    .pfx. Agrega sello de tiempo RFC3161 para que la firma siga siendo válida
    después de que el certificado expire.

    Por defecto firma ambos artefactos si existen:
      - dist\Margoth\Margoth.exe   (la app)
      - dist\Margoth_Setup.exe     (el instalador)

    Flujo recomendado de release:
      1. python build_exe.py                 # genera dist\Margoth\
      2. tools\sign.ps1 -AppOnly              # firma Margoth.exe
      3. ISCC margoth_installer.iss           # empaqueta el .exe YA firmado
      4. tools\sign.ps1 -InstallerOnly        # firma Margoth_Setup.exe

.PARAMETER Subject
    CN del certificado a usar (por defecto "Carlos G").

.PARAMETER TimestampServer
    Servidor de sello de tiempo RFC3161.
#>
param(
    [string]$Subject = "Carlos G",
    [string]$TimestampServer = "http://timestamp.digicert.com",
    [switch]$AppOnly,
    [switch]$InstallerOnly
)

$ErrorActionPreference = "Stop"
$root = Split-Path -Parent $PSScriptRoot

$cert = Get-ChildItem Cert:\CurrentUser\My -CodeSigningCert |
    Where-Object { $_.Subject -eq "CN=$Subject" } |
    Sort-Object NotAfter -Descending |
    Select-Object -First 1

if (-not $cert) {
    throw "No se encontró un certificado de firma con CN=$Subject. Corre primero tools\New-CodeSigningCert.ps1."
}
Write-Host "Firmando con: $($cert.Subject)  [$($cert.Thumbprint)]"

$targets = @()
if (-not $InstallerOnly) { $targets += (Join-Path $root "dist\Margoth\Margoth.exe") }
if (-not $AppOnly)       { $targets += (Join-Path $root "dist\Margoth_Setup.exe") }

foreach ($file in $targets) {
    if (-not (Test-Path $file)) {
        Write-Host "  (omitido, no existe) $file"
        continue
    }
    $res = Set-AuthenticodeSignature -FilePath $file -Certificate $cert `
        -TimestampServer $TimestampServer -HashAlgorithm SHA256
    Write-Host "  $($res.Status)  ->  $file"
    if ($res.Status -ne "Valid") {
        throw "La firma de $file falló: $($res.StatusMessage)"
    }
}

Write-Host "Firma completada."
