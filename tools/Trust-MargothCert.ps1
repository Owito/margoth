<#
.SYNOPSIS
    Instala el certificado público de Margoth como CONFIABLE en este equipo.

.DESCRIPTION
    Correr UNA vez en cada equipo donde se vaya a instalar Margoth. Importa
    `Margoth-CodeSigning.cer` a:
      - Entidades de certificación raíz de confianza  (valida la cadena)
      - Editores de confianza                          (reconoce al editor)

    Tras esto, la firma de Margoth.exe y de Margoth_Setup.exe aparece como
    VÁLIDA y desaparece el aviso de "Editor desconocido".

    NOTA: al importar a la raíz de confianza, Windows mostrará un cuadro de
    seguridad pidiendo confirmación. Es normal: acepta para completar.

.PARAMETER CerPath
    Ruta al archivo .cer público. Por defecto, junto a este script en signing\.

.PARAMETER AllUsers
    Instala para TODOS los usuarios del equipo (requiere ejecutar como
    administrador). Sin este switch, se instala solo para el usuario actual.
#>
param(
    [string]$CerPath,
    [switch]$AllUsers
)

$ErrorActionPreference = "Stop"

if (-not $CerPath) {
    $root = Split-Path -Parent $PSScriptRoot
    $CerPath = Join-Path $root "signing\Margoth-CodeSigning.cer"
}
if (-not (Test-Path $CerPath)) {
    throw "No se encontró el certificado: $CerPath"
}

$scope = if ($AllUsers) { "LocalMachine" } else { "CurrentUser" }
Write-Host "Instalando confianza del certificado ($scope) desde: $CerPath"

Import-Certificate -FilePath $CerPath -CertStoreLocation "Cert:\$scope\Root" | Out-Null
Import-Certificate -FilePath $CerPath -CertStoreLocation "Cert:\$scope\TrustedPublisher" | Out-Null

Write-Host "Listo. El certificado de Margoth ahora es de confianza en este equipo."
