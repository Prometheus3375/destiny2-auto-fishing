$VenvDirName = ".venv"
$DistDirName = ".dist"
$ExeDirName = "exe"
$PackageDirName = "destiny2autofishing"
$LatestTagName = "latest"

Set-Location $PSScriptRoot
& "$VenvDirName/Scripts/Activate.ps1"
python -m build -o $DistDirName
& "$ExeDirName/build-exe.ps1"

$Version = ((Get-Content "$PSScriptRoot/$PackageDirName/__init__.py") -Split "'", 3)[1]
$Version = "v$Version"
Write-Host "Package version is '$Version'. Press Enter to proceed"
Read-Host

git push origin :refs/tags/$LatestTagName
git tag $LatestTagName
git tag $Version
git push origin $LatestTagName
git push origin $Version
