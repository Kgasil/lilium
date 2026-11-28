param([Parameter(Mandatory=$true)][string]$Bundle,[Parameter(Mandatory=$true)][string]$Archive,[Parameter(Mandatory=$true)][string]$Evidence)
$ErrorActionPreference='Stop'
if ($env:GITHUB_ACTIONS -ne 'true' -or $env:RUNNER_ENVIRONMENT -ne 'github-hosted') { throw 'Disposable hosted runner required' }
$bundlePath=(Resolve-Path -LiteralPath $Bundle).Path
$zip=(Resolve-Path -LiteralPath $Archive).Path
$exe=Join-Path $bundlePath 'Lilium.exe'
$e=(Resolve-Path -LiteralPath $Evidence).Path
$targets=@($zip,$exe,$bundlePath)
$r=[ordered]@{commit=$env:GITHUB_SHA;status='INCONCLUSIVE';release_approved=$false;archive_sha256=(Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant();defender=@();clamav=@()}
try {
  $status=Get-MpComputerStatus -ErrorAction Stop
  if(-not $status.AntivirusEnabled -or -not $status.AMServiceEnabled){throw 'Defender inactive'}
  Update-MpSignature -ErrorAction Stop | Out-Null
  $status=Get-MpComputerStatus -ErrorAction Stop
  if(-not $status.AntivirusEnabled -or -not $status.AMServiceEnabled -or -not $status.AntivirusSignatureLastUpdated){throw 'Defender state incomplete'}
  $age=([DateTime]::UtcNow-([DateTime]$status.AntivirusSignatureLastUpdated).ToUniversalTime()).TotalSeconds
  if($age -lt 0 -or $age -gt 86400){throw 'Defender signatures stale'}
  $r['defender_signature_version']=$status.AntivirusSignatureVersion
  $r['defender_definition_age_seconds']=$age
  $platform=Join-Path $env:ProgramData 'Microsoft\Windows Defender\Platform'
  $cmd=Get-ChildItem -LiteralPath $platform -Directory | Sort-Object LastWriteTime -Descending | ForEach-Object {Join-Path $_.FullName 'MpCmdRun.exe'} | Where-Object {Test-Path -LiteralPath $_ -PathType Leaf} | Select-Object -First 1
  if(-not $cmd -or (Get-AuthenticodeSignature -LiteralPath $cmd).Status -ne 'Valid'){throw 'Trusted Defender unavailable'}
  $i=0
  foreach($target in $targets){
    $i++;$log=Join-Path $e "defender-$i.log";$err=Join-Path $e "defender-$i-error.log"
    $p=Start-Process -FilePath $cmd -ArgumentList @('-Scan','-ScanType','3','-File',('"'+$target+'"')) -RedirectStandardOutput $log -RedirectStandardError $err -PassThru
    if(-not $p.WaitForExit(180000)){throw 'Defender timeout'}
    $out=Get-Content -LiteralPath $log -Raw;$stderr=Get-Content -LiteralPath $err -Raw
    if($p.ExitCode -ne 0 -or $out -match '(?im)\b(?:skipped|not scanned|excluded)\b' -or -not [string]::IsNullOrWhiteSpace($stderr) -or @($out -split '\r?\n' | Where-Object {$_.Trim() -ceq ('Scanning '+$target+' found no threats.')}).Count -ne 1){throw 'Defender scan incomplete or failed'}
    $r.defender+=@([pscustomobject]@{target=(Split-Path -Leaf $target);outcome='COMPLETED_NO_THREATS_REPORTED';exit_code=$p.ExitCode})
  }
  $hits=@(Get-MpThreatDetection -ErrorAction Stop|Where-Object {@($_.Resources|Where-Object {$_ -and ($_.IndexOf($bundlePath,[StringComparison]::OrdinalIgnoreCase) -ge 0 -or $_.IndexOf($zip,[StringComparison]::OrdinalIgnoreCase) -ge 0)}).Count -gt 0})
  if($hits.Count){throw 'Defender detection requires review'}
  $engine=$env:LILIUM_CLAM_ENGINE;$db=$env:LILIUM_CLAM_DB
  if(-not $engine -or -not $db){throw 'Signed preflight scanner missing'}
  $daily=@(Get-ChildItem -LiteralPath $db -File|Where-Object {$_.Name -in @('daily.cvd','daily.cld')})
  if($daily.Count -ne 1){throw 'Daily database ambiguous'}
  $sig=Join-Path $engine 'sigtool.exe'
  $info=(& $sig --info $daily[0].FullName|Out-String)
  $info|Set-Content -LiteralPath (Join-Path $e 'clamav-daily-info.txt') -Encoding utf8
  if($LASTEXITCODE -ne 0 -or $info -notmatch '(?m)^Verification OK\.?\s*$' -or $info -notmatch '(?m)^Build time:\s*(.+)$'){throw 'ClamAV signature/time invalid'}
  $raw=$Matches[1].Trim() -replace '([+-]\d{2})(\d{2})$','$1:$2'
  $date=[DateTimeOffset]::ParseExact($raw,'dd MMM yyyy HH:mm zzz',[Globalization.CultureInfo]::InvariantCulture)
  $age=([DateTimeOffset]::UtcNow-$date).TotalSeconds
  if($age -lt 0 -or $age -gt 86400){throw 'ClamAV definitions stale'}
  $r['clamav_definition_age_seconds']=$age
  $r['clamav_definition_build_utc']=$date.ToUniversalTime().ToString('o')
  $i=0
  foreach($target in $targets){
    $i++;$log=Join-Path $e "clamav-$i.log"
    $PSNativeCommandUseErrorActionPreference=$false
    & (Join-Path $engine 'clamscan.exe') "--database=$db" '--recursive=yes' '--scan-archive=yes' '--alert-exceeds-max=yes' '--max-filesize=100M' '--max-scansize=400M' '--max-files=20000' '--max-recursion=30' $target 2>&1|ForEach-Object {"$_"}|Set-Content -LiteralPath $log -Encoding utf8
    $exit=$LASTEXITCODE;$out=Get-Content -LiteralPath $log -Raw
    if($exit -ne 0 -or $out -notmatch '(?m)^Infected files:\s*0\s*$' -or $out -notmatch '(?m)^Scanned files:\s*[1-9]\d*\s*$' -or $out -match '(?im)\b(?:ERROR|WARNING|skipped|excluded)\b|\sFOUND\s*$'){throw 'ClamAV incomplete, alert or detection'}
    $r.clamav+=@([pscustomobject]@{target=(Split-Path -Leaf $target);outcome='COMPLETED_NO_THREATS_REPORTED';exit_code=$exit})
  }
  if(([DateTimeOffset]::UtcNow-$date).TotalSeconds -gt 86400){throw 'ClamAV definitions aged out during scan'}
  if((Get-FileHash -LiteralPath $zip -Algorithm SHA256).Hash.ToLowerInvariant() -cne $r.archive_sha256){throw 'Candidate archive changed'}
  $r.status='COMPLETE_NO_THREATS_REPORTED'
} catch {$r['error']=$_.Exception.Message;throw}
finally {$r|ConvertTo-Json -Depth 8|Set-Content -LiteralPath (Join-Path $e 'candidate-scans.json') -Encoding utf8}
