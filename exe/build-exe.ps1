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
    --exclude-module pytweening `
    --exclude-module pymsgbox `
    --exclude-module pyscreeze `
    --exclude-module mouseinfo `
    --exclude-module pygetwindow `
    --exclude-module pyautogui._pyautogui_java `
    --exclude-module pyautogui._pyautogui_osx `
    --exclude-module pyautogui._pyautogui_x11 `
    --exclude-module PIL.BlpImagePlugin `
    --exclude-module PIL.BmpImagePlugin `
    --exclude-module PIL.BufrStubImagePlugin `
    --exclude-module PIL.CurImagePlugin `
    --exclude-module PIL.DcxImagePlugin `
    --exclude-module PIL.DdsImagePlugin `
    --exclude-module PIL.EpsImagePlugin `
    --exclude-module PIL.FitsImagePlugin `
    --exclude-module PIL.FitsStubImagePlugin `
    --exclude-module PIL.FliImagePlugin `
    --exclude-module PIL.FpxImagePlugin `
    --exclude-module PIL.FtexImagePlugin `
    --exclude-module PIL.GbrImagePlugin `
    --exclude-module PIL.GifImagePlugin `
    --exclude-module PIL.GribStubImagePlugin `
    --exclude-module PIL.Hdf5StubImagePlugin `
    --exclude-module PIL.IcnsImagePlugin `
    --exclude-module PIL.IcoImagePlugin `
    --exclude-module PIL.ImImagePlugin `
    --exclude-module PIL.ImtImagePlugin `
    --exclude-module PIL.IptcImagePlugin `
    --exclude-module PIL.JpegImagePlugin `
    --exclude-module PIL.Jpeg2KImagePlugin `
    --exclude-module PIL.McIdasImagePlugin `
    --exclude-module PIL.MicImagePlugin `
    --exclude-module PIL.MpegImagePlugin `
    --exclude-module PIL.MpoImagePlugin `
    --exclude-module PIL.MspImagePlugin `
    --exclude-module PIL.PalmImagePlugin `
    --exclude-module PIL.PcdImagePlugin `
    --exclude-module PIL.PcxImagePlugin `
    --exclude-module PIL.PdfImagePlugin `
    --exclude-module PIL.PixarImagePlugin `
    --exclude-module PIL.PpmImagePlugin `
    --exclude-module PIL.PsdImagePlugin `
    --exclude-module PIL.QoiImagePlugin `
    --exclude-module PIL.SgiImagePlugin `
    --exclude-module PIL.SpiderImagePlugin `
    --exclude-module PIL.SunImagePlugin `
    --exclude-module PIL.TgaImagePlugin `
    --exclude-module PIL.TiffImagePlugin `
    --exclude-module PIL.WebPImagePlugin `
    --exclude-module PIL.WmfImagePlugin `
    --exclude-module PIL.XbmImagePlugin `
    --exclude-module PIL.XpmImagePlugin `
    --exclude-module PIL.XVThumbImagePlugin `
    --exclude-module PIL.PyAccess `
    --exclude-module PIL.ImageCms `
    --exclude-module PIL.ImageFilter `
    --exclude-module PIL.ImageQt `
    --exclude-module PIL.ImageShow `
    --console `
    --icon icon.ico `
    --version-file version-info.py `
    --onefile

python -m "$ThisDirName.make_zip" $DistDirName

Write-Host "`nExecutable is built sucessfully`n"
