param([Parameter(Mandatory=$true)][string]$Path,[switch]$Foreign)
$ErrorActionPreference='Stop'
# Test-only: operate on disposable runner fixture, never real owner directory.
if ($env:GITHUB_ACTIONS -ne 'true') { throw 'CI fixture only' }
$full=(Get-Item -LiteralPath $Path).FullName
if (-not $full.StartsWith([IO.Path]::GetTempPath(),[StringComparison]::OrdinalIgnoreCase)) { throw 'Temporary fixture required' }
$me=[Security.Principal.WindowsIdentity]::GetCurrent().User
$acl=[Security.AccessControl.DirectorySecurity]::new()
$acl.SetOwner($me)
$acl.SetAccessRuleProtection($true,$false)
$flags=[Security.AccessControl.InheritanceFlags]'ContainerInherit,ObjectInherit'
foreach ($sid in @($me.Value,'S-1-5-18','S-1-5-32-544')) {
    $rule=[Security.AccessControl.FileSystemAccessRule]::new([Security.Principal.SecurityIdentifier]::new($sid),'FullControl',$flags,'None','Allow')
    $acl.AddAccessRule($rule)
}
if ($Foreign) { $acl.AddAccessRule([Security.AccessControl.FileSystemAccessRule]::new([Security.Principal.SecurityIdentifier]::new('S-1-1-0'),'ReadAndExecute',$flags,'None','Allow')) }
Set-Acl -LiteralPath $full -AclObject $acl
