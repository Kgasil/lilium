param([Parameter(Mandatory=$true)][string]$Bundle,[Parameter(Mandatory=$true)][string]$PythonRoot,[Parameter(Mandatory=$true)][string]$Output)
$ErrorActionPreference='Stop'
$root=(Resolve-Path -LiteralPath $Bundle).Path
$source=(Resolve-Path -LiteralPath $PythonRoot).Path
$pattern='^(vcruntime|msvcp|msvcr|concrt|vcomp|ucrtbase|api-ms-win-crt|mfc|atl|vccorlib).*\.dll$'
$rows=@(Get-ChildItem -LiteralPath $root -File -Recurse | Where-Object { $_.Name -match $pattern } | ForEach-Object {
    $p=$_
    $sha=(Get-FileHash -LiteralPath $p.FullName -Algorithm SHA256).Hash.ToLowerInvariant()
    $sig=Get-AuthenticodeSignature -LiteralPath $p.FullName
    $matches=@(Get-ChildItem -LiteralPath $source -File -Recurse -Filter $p.Name | Where-Object { (Get-FileHash -LiteralPath $_.FullName -Algorithm SHA256).Hash.ToLowerInvariant() -eq $sha } | ForEach-Object { $_.FullName.Substring($source.Length).TrimStart('\') })
    [ordered]@{path=$p.FullName.Substring($root.Length).TrimStart('\');sha256=$sha;bytes=$p.Length;file_version=$p.VersionInfo.FileVersion;product_version=$p.VersionInfo.ProductVersion;signature_status=[string]$sig.Status;signer=if($sig.SignerCertificate){$sig.SignerCertificate.Subject}else{$null};matching_python_source_paths=$matches;redistribution_rights='REVIEW_REQUIRED'}
})
[ordered]@{schema='lilium.microsoft-inventory.v1';scope='Named Microsoft runtime DLL candidates only, not proof of all linked code';files=$rows;license_clearance='NOT_TESTED';release_approved=$false} | ConvertTo-Json -Depth 6 | Set-Content -LiteralPath $Output -Encoding utf8
