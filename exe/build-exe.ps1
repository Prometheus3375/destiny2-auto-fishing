$ThisDir = $PSScriptRoot
$ThisDirName = Split-Path $ThisDir -Leaf
$RootDir = Split-Path $ThisDir -Parent
$VenvDirName = ".venv"
$DistDirName = ".dist"

cd $RootDir
& "$VenvDirName/Scripts/Activate.ps1"
python -m "$ThisDirName.make_version_info"
pyinstaller "$ThisDir/main.py" `
    --distpath $DistDirName `
    --workpath "$ThisDir/.build" `
    --noconfirm `
    --clean `
    --specpath $ThisDir `
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

# todo get all files from destiny2autofishing/predefined
#  create zip file, add there exe and predefined files to 'configs' directory
#  can be done via python script
