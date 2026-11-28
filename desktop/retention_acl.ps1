param([Parameter(Mandatory=$true)][string]$Path,[switch]$Root)
$ErrorActionPreference='Stop'
$item=Get-Item -LiteralPath $Path -Force
$full=$item.FullName
$drive=[System.IO.DriveInfo]::new([System.IO.Path]::GetPathRoot($full))
if ($drive.DriveType -ne 'Fixed' -or $drive.DriveFormat -ne 'NTFS') { throw 'Local fixed NTFS required' }
$cursor=$item
while ($null -ne $cursor) {
    if ($cursor.Attributes -band [IO.FileAttributes]::ReparsePoint) { throw 'Reparse point refused' }
    if ($cursor -is [IO.DirectoryInfo]) { $cursor=$cursor.Parent } else { $cursor=$cursor.Directory }
}
$me=[Security.Principal.WindowsIdentity]::GetCurrent().User
$allowed=@($me.Value,'S-1-5-18','S-1-5-32-544')
$acl=$item.GetAccessControl([Security.AccessControl.AccessControlSections]'Access,Owner')
$owner=$acl.GetOwner([Security.Principal.SecurityIdentifier]).Value
# Elevated Windows processes may create children owned by Builtin Administrators.
# Root must still be user-owned; trusted child owner never grants access to another ordinary principal.
if ($Root -and $owner -ne $me.Value) { throw 'Current user must own retention root' }
if (-not $Root -and $owner -notin @($me.Value,'S-1-5-32-544')) { throw 'Unexpected child owner' }
if ($Root -and (-not $item.PSIsContainer -or -not $acl.AreAccessRulesProtected)) { throw 'Root must be directory with protected DACL' }
$rules=@($acl.GetAccessRules($true,$true,[Security.Principal.SecurityIdentifier]))
$fullControl=[Security.AccessControl.FileSystemRights]::FullControl
$inherit=[Security.AccessControl.InheritanceFlags]::ContainerInherit -bor [Security.AccessControl.InheritanceFlags]::ObjectInherit
$own=$false
foreach ($rule in $rules) {
    if ($rule.AccessControlType -eq 'Allow') {
        if ($rule.IdentityReference.Value -notin $allowed) { throw 'Unapproved access principal' }
        if ($rule.IdentityReference.Value -eq $me.Value -and ($rule.FileSystemRights -band $fullControl) -eq $fullControl -and -not ($rule.PropagationFlags -band [Security.AccessControl.PropagationFlags]::InheritOnly)) {
            if (-not $Root -or (($rule.InheritanceFlags -band $inherit) -eq $inherit -and $rule.PropagationFlags -eq 'None')) { $own=$true }
        }
    } else { throw 'Unexpected deny ACE; manual review required' }
}
if (-not $own) { throw 'Explicit owner full control required' }
Write-Output 'ACL_PASS'
