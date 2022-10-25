@echo off

tasklist /fi "imagename eq chrome.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "chrome.exe" /T

tasklist /fi "imagename eq backend.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "backend.exe"

tasklist /fi "imagename eq mongodump.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "mongodump.exe"

tasklist /fi "imagename eq mongo.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "mongo.exe"

tasklist /fi "imagename eq mongorestore.exe" |find ":" > nul
if errorlevel 1 taskkill /f /im "mongorestore.exe"

if exist "C:\Windows\tasskkill.bat" del "C:\Windows\tasskkill.bat"
if exist "C:\Windows\leodeploy.bat" del "C:\Windows\leodeploy.bat"

cd /d "D:\Program Files\Lumenis\Leo\bin\LEO_RF_MCU_Simulator"
start "" "LeoRfMcuSimulator.exe"

timeout 2
cd /d "D:\Program Files\Lumenis\Leo\bin\ServicesOrchestrator"
start "" "ServicesOrchestrator.exe"

timeout 3
cd /d "D:\Program Files\Lumenis\Leo\bin"
start "" "backend.exe"

"C:\Program Files\Google\Chrome\Application\chrome.exe" --start-fullscreen -incognito "http://localhost:8080"
exit
