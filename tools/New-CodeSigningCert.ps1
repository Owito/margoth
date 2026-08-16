<#
.SYNOPSIS
    Crea un certificado de firma de código AUTO-FIRMADO para Margoth.

.DESCRIPTION
    Uso interno: firmar Margoth para equipos que tú controlas. NO sirve para
    quitar SmartScreen en distribución pública (eso requiere un certificado EV
    comprado). El certificado queda en el almacén del usuario (Cert:\CurrentUser\My)
    y se exportan dos archivos en la carpeta `signing/`:

      - Margoth-CodeSigning.cer  -> PÚBLICO. Se instala en los equipos destino
                                    para "confiar" en la firma.
      - Margoth-CodeSigning.pfx  -> PRIVADO (con contraseña). Respáldalo; permite
                                    firmar desde otro equipo. NO se sube al repo.

    Correr una sola vez. Válido por 5 años.

.PARAMETER PfxPassword
    Contraseña para proteger el .pfx exportado (respaldo de la clave privada).

.PARAMETER Publisher
    Nombre del editor (CN del certificado). Debe coincidir con AppPublisher del
    instalador para que la identidad sea consistente.
#>
param(
    [Parameter(Mandatory = $true)]
    [string]$PfxPassword,

    [string]$Publisher = "Carlos G",

    [int]$YearsValid = 5
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$outDir = Join-Path $root "signing"
New-Item -ItemType Directory -Force -Path $outDir | Out-Null

Write-Host "Creando certificado de firma de código para '$Publisher'..."
$cert = New-SelfSignedCertificate `
    -Type CodeSigningCert `
    -Subject "CN=$Publisher" `
    -FriendlyName "Margoth Code Signing" `
    -CertStoreLocation "Cert:\CurrentUser\My" `
    -KeyUsage DigitalSignature `
    -KeyExportPolicy Exportable `
    -NotAfter (Get-Date).AddYears($YearsValid)

Write-Host "  Thumbprint: $($cert.Thumbprint)"

$cerPath = Join-Path $outDir "Margoth-CodeSigning.cer"
$pfxPath = Join-Path $outDir "Margoth-CodeSigning.pfx"

Export-Certificate -Cert $cert -FilePath $cerPath | Out-Null
$secure = ConvertTo-SecureString -String $PfxPassword -Force -AsPlainText
Export-PfxCertificate -Cert $cert -FilePath $pfxPath -Password $secure | Out-Null

Write-Host ""
Write-Host "Listo:"
Write-Host "  Público (repartir a equipos): $cerPath"
Write-Host "  Privado (respaldar, NO subir): $pfxPath"
Write-Host "  Thumbprint para firmar:        $($cert.Thumbprint)"
