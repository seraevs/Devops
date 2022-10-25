@echo off
rem =================================
rem =================================
rem ======== The batch script  ======
rem ========== Deployment ===========
rem === Build by Sergey Yvstigneev ==
rem =================================
rem =================================

set "JENKINS_PATH=F:\jenkins\workspace\LeoPrj"
set "PSTOOLS=D:\Soft\PSTools\PsExec.exe"
set "PSTOOLSSHUTDOWN=D:\Soft\PSTools\psshutdown.exe"
set IP_ADDRESS=%1

echo Y | net use x: /d
net use x: \\%IP_ADDRESS%\d /user:clinicaluser User1234

%PSTOOLSSHUTDOWN% \\%IP_ADDRESS% -r -u "clinicaluser" -p "User1234" /t 0

:pingtheserver
ping %IP_ADDRESS% | find "Reply" > nul
if not errorlevel 1 (
    echo "server is online, up and running."
	goto :start
) else (my
    echo host has been taken down wait 2 seconds to refresh
    ping %IP_ADDRESS% -n 1 -w 2000 >NUL
    goto :pingtheserver
) 

:start
echo Y | net use x: /d
net use x: \\%IP_ADDRESS%\d /user:clinicaluser User1234

if exist "\\%IP_ADDRESS%\c\Windows\leodeploy.bat" del "\\%IP_ADDRESS%\c\Windows\leodeploy.bat"
if exist "\\%IP_ADDRESS%\c\Windows\runAll.bat" del "\\%IP_ADDRESS%\c\Windows\runAll.bat"
if not exist "%JENKINS_PATH%\bin" rd /S /Q "%JENKINS_PATH%\bin"
if not exist "%JENKINS_PATH%\bin" mkdir "%JENKINS_PATH%\bin"
if not exist "%JENKINS_PATH%\bin\DataBaseConfiguration" mkdir "%JENKINS_PATH%\bin\DataBaseConfiguration"
if not exist "%JENKINS_PATH%\bin\LEO_RF_MCU_Simulator" mkdir "%JENKINS_PATH%\bin\LEO_RF_MCU_Simulator"

echo D | xcopy "%JENKINS_PATH%\unified\DataBaseConfiguration" "%JENKINS_PATH%\bin\DataBaseConfiguration" /s /e
echo D | xcopy "%JENKINS_PATH%\unified\bin" "%JENKINS_PATH%\bin" /s /e
echo D | xcopy "%JENKINS_PATH%\Leo\bin" "%JENKINS_PATH%\bin" /s /e
echo D | xcopy "%JENKINS_PATH%\Leo\Simulators\LeoRfMcuSimulator\bin\Debug\net6.0" "%JENKINS_PATH%\bin\LEO_RF_MCU_Simulator" /s /e
if exist "%JENKINS_PATH%\bin\ControllerSimulator.exe" del "%JENKINS_PATH%\bin\ControllerSimulator.exe"

if exist "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo_Backup" rd /S /Q  "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo_Backup"
if not exist "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo_Backup" mkdir "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo_Backup"
echo D | xcopy "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo" "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo_Backup"  /s /e
if exist "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo" rd /S /Q  "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo"
if not exist "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo" mkdir "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo"

if not exist   "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\bin" mkdir "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\bin"
if not exist   "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\DataBaseConfiguration" mkdir "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\DataBaseConfiguration"
echo D | xcopy "%JENKINS_PATH%\bin\DataBaseConfiguration" "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\DataBaseConfiguration"  /s /e
echo D | xcopy "%JENKINS_PATH%\bin" "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\bin"  /s /e

echo F | xcopy "%JENKINS_PATH%\scripts\tech\runAll.bat" "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\bin\runAll.bat" /s /e
echo F | xcopy "%JENKINS_PATH%\scripts\tech\leodeploy.bat" "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\leodeploy.bat" /s /e

for /f "tokens=*" %%a in (F:\\jenkins\\workspace\\Config\\leo.txt) do (set %%a)	
set "ckhecklist=false"

if not exist "\\%IP_ADDRESS%\d\\Program Files\Lumenis\Leo\bin\LEO_RF_MCU_Simulator\LeoRfMcuSimulator.exe" (echo "file not exists LeoRfMcuSimulator.exe" && set "ckhecklist=true")
if not exist "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\\bin\ServicesOrchestrator\ServicesOrchestrator.exe" (echo "file not exists ServicesOrchestrator.exe" && set "ckhecklist=true")
if not exist "\\%IP_ADDRESS%\d\\Program Files\Lumenis\Leo\bin\backend.exe" (echo "file not exists backend.exe" && set "ckhecklist=true")

if exist "\\%IP_ADDRESS%\c\Windows\leodeploy.bat" del "\\%IP_ADDRESS%\c\Windows\leodeploy.bat"
%PSTOOLS% \\%IP_ADDRESS% -u "clinicaluser" -p "User1234" -i -d -c  "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\leodeploy.bat"

if not exist "%JENKINS_PATH%\scripts\tech\LumenisXServiceInstall 2.0.5.msi" echo F | xcopy "%JENKINS_PATH%\scripts\tech\LumenisXServiceInstall 2.0.5.msi" "\\%IP_ADDRESS%\d\Program Files"  /s /e
if exist "\\%IP_ADDRESS%\c\Windows\LumXinstall.bat" del "\\%IP_ADDRESS%\c\Windows\LumXinstall.bat"
echo F | xcopy "%JENKINS_PATH%\scripts\tech\LumXinstall.bat" "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\bin\LumXinstall.bat" /s /e
%PSTOOLS% \\%IP_ADDRESS% -u "clinicaluser" -p "User1234" -i -d -c  "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\bin\LumXinstall.bat"

if exist "\\%IP_ADDRESS%\c\Windows\runAll.bat" del "\\%IP_ADDRESS%\c\Windows\runAll.bat"
%PSTOOLS% \\%IP_ADDRESS% -u "clinicaluser" -p "User1234" -i -d -c  "\\%IP_ADDRESS%\d\Program Files\Lumenis\Leo\bin\runAll.bat"
timeout 3
tasklist.exe /S %IP_ADDRESS% /U "clinicaluser" /P "User1234" /FI "ImageName eq backend.exe" /v /fo List 2>NUL | find /I "backend.exe">NUL			
if "%ERRORLEVEL%"=="0" (echo "file not running backend.exe" && set "ckhecklist=true")

if "%ckhecklist%" == "false" (%PSTOOLSSHUTDOWN% \\%IP_ADDRESS% -r -u "clinicaluser" -p "User1234" /t 0)

if "%ckhecklist%" == "true" (echo "file not running backend.exe" && python %SEND_MANAGER_MAIL% "Deployment" && explorer "\\%IP_ADDRESS%\s\errors" && exit /b)
