@echo off

:: Blander folder
set "BLENDER_PATH=C:\Users\sover\Desktop\blender\blender-3.5.1-windows-x64"

:: Addon path
set "ADDON_SOURCE=ufit"  REM Local folder of addon
set "ADDON_DEST=%BLENDER_PATH%\3.5\scripts\addons\ufit"  REM Target folder

:: Remove the ufit folder and its contents
if exist "%ADDON_DEST%" (
    rmdir /s /q "%ADDON_DEST%"
)

:: Recreate the ufit folder
mkdir "%ADDON_DEST%"

:: Copy the contents of the local ufit folder to the destination
xcopy /E /Y "%ADDON_SOURCE%" "%ADDON_DEST%"

:: Rename the __init_plugins__.py file to __init__.py
if exist "%ADDON_DEST%\__init_plugins__.py" (
    ren "%ADDON_DEST%\__init_plugins__.py" "__init__.py"
)

:: Terminate Blender
taskkill /F /IM blender.exe >nul 2>&1

:: Start Blender
"%BLENDER_PATH%\blender.exe"
pause