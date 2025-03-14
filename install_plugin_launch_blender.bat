@echo off
setlocal EnableDelayedExpansion

:: Load environment variables from .env file
if exist .env (
    for /F "tokens=*" %%A in (.env) do (
        set %%A
    )
)

:: Check required environment variables
set "required_vars=BLENDER_EXECUTABLE_PATH BLENDER_ADDONS_PATH ANACONDA_PATH CONDA_ENV_NAME"
set "missing_vars="

for %%v in (%required_vars%) do (
    if not defined %%v (
        set "missing_vars=!missing_vars! %%v"
    )
)

if defined missing_vars (
    echo Error: Missing required environment variables:%missing_vars%
    exit /b 1
)

echo ================================
echo Using environment variables:
echo BLENDER_ADDONS_PATH: %BLENDER_ADDONS_PATH%
echo ANACONDA_PATH: %ANACONDA_PATH%
echo CONDA_ENV_NAME: %CONDA_ENV_NAME%

:: Activate Conda environment
call "%ANACONDA_PATH%\Scripts\activate.bat" %CONDA_ENV_NAME%

:: Remove existing plugin and copy new version
rmdir /s /q "%BLENDER_ADDONS_PATH%\ufit" 2>nul
mkdir "%BLENDER_ADDONS_PATH%\ufit"
xcopy /s /e /y ufit\* "%BLENDER_ADDONS_PATH%\ufit\"

:: Kill Blender process if running
taskkill /IM blender.exe /F 2>nul

echo ================================

:: Start Blender with system environment
start "" "%BLENDER_EXECUTABLE_PATH%" --python-use-system-env
