@echo off
title WebP Converter Pro Installer
echo ========================================================
echo        WebP Converter Pro - Auto Unblock & Setup
echo ========================================================
echo.

set "EXE_NAME=WebP Converter Pro.exe"
set "SRC_PATH=%~dp0%EXE_NAME%"
set "DEST_DIR=%LOCALAPPDATA%\Programs\WebP Converter Pro"
set "DEST_PATH=%DEST_DIR%\%EXE_NAME%"

echo [1/3] Removing Windows Mark of the Web (Zone.Identifier)...
powershell -Command "Unblock-File -Path '%SRC_PATH%' -ErrorAction SilentlyContinue"

echo [2/3] Installing application to %DEST_DIR%...
if not exist "%DEST_DIR%" mkdir "%DEST_DIR%"
copy /Y "%SRC_PATH%" "%DEST_PATH%" >nul
powershell -Command "Unblock-File -Path '%DEST_PATH%' -ErrorAction SilentlyContinue"

echo [3/3] Creating Desktop and Start Menu Shortcuts...
powershell -Command "$s=(New-Object -COM WScript.Shell).CreateShortcut([System.IO.Path]::Combine([Environment]::GetFolderPath('Desktop'), 'WebP Converter Pro.lnk')); $s.TargetPath='%DEST_PATH%'; $s.WorkingDirectory='%DEST_DIR%'; $s.Save()"
powershell -Command "$sm=[System.IO.Path]::Combine([Environment]::GetFolderPath('StartMenu'), 'Programs'); $s=(New-Object -COM WScript.Shell).CreateShortcut([System.IO.Path]::Combine($sm, 'WebP Converter Pro.lnk')); $s.TargetPath='%DEST_PATH%'; $s.WorkingDirectory='%DEST_DIR%'; $s.Save()"

echo.
echo ========================================================
echo SUCCESS! WebP Converter Pro has been installed cleanly.
echo Desktop & Start Menu shortcuts created and unblocked.
echo ========================================================
echo.
pause
