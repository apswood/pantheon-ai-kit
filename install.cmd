@echo off
rem install.cmd - Zero-clone bootstrap for Windows Command Prompt
rem Usage: curl -fsSL https://raw.githubusercontent.com/apswood/pantheon-ai-kit/main/install.cmd -o install.cmd && install.cmd && del install.cmd

setlocal enabledelayedexpansion

if "%PANTHEON_REF%"=="" (
    set "REF=main"
) else (
    set "REF=%PANTHEON_REF%"
)

echo ======================================================================
echo   PANTHEON AI SETUP KIT - WINDOWS CMD BOOTSTRAPPER
echo ======================================================================
echo   Release Reference: %REF%
echo.

where pwsh.exe >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [INFO] Launching via PowerShell 7 (pwsh.exe)...
    pwsh.exe -NoProfile -ExecutionPolicy Bypass -Command "$env:PANTHEON_REF='%REF%'; irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/%REF%/validate_and_install.ps1 | iex"
    exit /b %ERRORLEVEL%
)

where powershell.exe >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [INFO] Launching via Windows PowerShell...
    powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; $env:PANTHEON_REF='%REF%'; irm https://raw.githubusercontent.com/apswood/pantheon-ai-kit/%REF%/validate_and_install.ps1 | iex"
    exit /b %ERRORLEVEL%
)

where python.exe >nul 2>&1
if %ERRORLEVEL% equ 0 (
    echo [INFO] Launching via Python...
    curl -fsSL "https://raw.githubusercontent.com/apswood/pantheon-ai-kit/%REF%/setup.py" -o "%TEMP%\pantheon_setup.py"
    python "%TEMP%\pantheon_setup.py" --init-env --ref "%REF%"
    set PY_EXIT=%ERRORLEVEL%
    del "%TEMP%\pantheon_setup.py" >nul 2>&1
    exit /b %PY_EXIT%
)

echo [ERROR] Neither PowerShell nor Python was found on PATH.
echo         Please install PowerShell 7 or Python 3.10+ to continue.
exit /b 1
