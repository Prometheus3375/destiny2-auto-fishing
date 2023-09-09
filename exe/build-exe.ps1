$ThisDirName = Split-Path $PSScriptRoot -Leaf
$RootDir = Split-Path $PSScriptRoot -Parent
$VenvDirName = ".venv"
$DistDirName = ".dist"

Set-Location $RootDir
& "$VenvDirName/Scripts/Activate.ps1"
python -m "$ThisDirName.make_version_info"
pyinstaller "$PSScriptRoot/main.py" `
    --distpath $DistDirName `
    --workpath "$PSScriptRoot/.build" `
    --noconfirm `
    --clean `
    --specpath $PSScriptRoot `
    --name destiny2autofishing `
    --paths . `
    --exclude-module destiny2autofishing.predefined `
    --exclude-module tkinter `
    --exclude-module numpy.array_api `
    --exclude-module pyautogui._pyautogui_java `
    --exclude-module pyautogui._pyautogui_osx `
    --exclude-module pyautogui._pyautogui_x11 `
    --exclude-module pygetwindow._pygetwindow_macos.py `
    --console `
    --icon icon.ico `
    --version-file version-info.py `
    --onefile

python -m "$ThisDirName.make_zip" $DistDirName

Write-Host "`nExecutable is build sucessfully`n"
