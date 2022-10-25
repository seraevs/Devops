@echo off
rem =================================
rem =================================
rem ====== The batch CA script  =====
rem =========== SonarQube ===========
rem === Build by Sergey Yvstigneev ==
rem =================================
rem =================================

echo =========== Begin config section ===========
rem =========== Dinamic Confiuration ============
set JENKINS_PATH_ARCHIVE=F:\jenkins\workspace\LeoPrj
set JENKINS_PATH_SCRIPTS=F:\jenkins\workspace\LeoPrj\scripts
set SolutionDir="%JENKINS_PATH_ARCHIVE%\services"
set URL_PATH=http://xx.xx.xx.xx:9000
rem ============ Static Confiuration ============
set SONAR_SCANER_BAT=D:\soft\SonarWindows\sonar-scanner-cli-4.6.2.2472-windows\sonar-scanner-4.6.2.2472-windows\bin\sonar-scanner.bat
set VS_MsBuild=C:\Program Files\Microsoft Visual Studio\2022\Professional\Msbuild\Current\Bin\MsBuild.exe
set Sonar_MsBuild=D:\soft\SonarWindows\sonar-scanner-msbuild-5.4.1.41282-net46\SonarScanner.MSBuild.exe
set DEVNEV=C:\Program Files\Microsoft Visual Studio\2022\Professional\Common7\IDE\devenv.exe
set BUILD_WRAPER=D:\soft\SonarWindows\build-wrapper-win-x86\build-wrapper-win-x86-64.exe
echo ============ End config section ============

cd /d "%JENKINS_PATH_ARCHIVE%"

del /q /s  "%JENKINS_PATH_ARCHIVE%\.sonarqube\*.*"
rmdir /q /s "%JENKINS_PATH_ARCHIVE%\.sonarqube"

del /q /s  "%JENKINS_PATH_ARCHIVE%\unified\frontend\.scannerwork\*.*"
rmdir /q /s "%JENKINS_PATH_ARCHIVE%\unified\frontend\.scannerwork"


echo "=============== Run C# CA =================="
cd /d "%JENKINS_PATH_ARCHIVE%\unified\services"
dotnet sonarscanner begin /k:"Unified-Cs-NetCore" /d:sonar.host.url="%URL_PATH%"  /d:sonar.login="4a027c74a86385b7ee213950d05b291060b10cca"
dotnet build "%JENKINS_PATH_ARCHIVE%\unified\services\Services.sln"
dotnet sonarscanner end /d:sonar.login="4a027c74a86385b7ee213950d05b291060b10cca"
echo "================ END C# CA =================="

echo "====== Run Leo-Cs-RF_Host_Simulator CA ======"
cd /d "%JENKINS_PATH_ARCHIVE%\Leo\Simulators\LEO_RF_Host_Simulator"
dotnet sonarscanner begin /k:"Leo-Cs-RF_Host_Simulator" /d:sonar.host.url="http://10.11.235.6:9000"  /d:sonar.login="6a0db2874e06f33d82fca8cc5e4d5124d99c3d1c"
dotnet build "%JENKINS_PATH_ARCHIVE%\Leo\Simulators\LEO_RF_Host_Simulator\LEO_RF_Host_Simulator.csproj"
dotnet sonarscanner end /d:sonar.login="6a0db2874e06f33d82fca8cc5e4d5124d99c3d1c"
echo "====== END Leo-Cs-RF_Host_Simulator CA ======"

echo "======== Run LEO_RF_MCU_Simulator CA ========"
cd /d "%JENKINS_PATH_ARCHIVE%\Leo\Simulators\LEO_RF_MCU_Simulator"
dotnet sonarscanner begin /k:"Leo-Cs-RF_MCU_Simulator" /d:sonar.host.url="http://10.11.235.6:9000"  /d:sonar.login="57f5d32d7b57cf8ae3690abcaa9fff596bda5d4e"
dotnet build "%JENKINS_PATH_ARCHIVE%\Leo\Simulators\LEO_RF_MCU_Simulator\LEO_RF_MCU_Simulator.csproj"
dotnet sonarscanner end /d:sonar.login="57f5d32d7b57cf8ae3690abcaa9fff596bda5d4e"
echo "======== END LEO_RF_MCU_Simulator CA ========"

echo "============== Begin unified-c++ ============"
cd /d "%JENKINS_PATH_ARCHIVE%\unified\services"
call %BUILD_WRAPER% --out-dir bw-output %DEVNEV% "%JENKINS_PATH_ARCHIVE%\services\ControllerSimulator.sln" /Rebuild "Release|x64" /Out "UnifiedBuildLog.txt"
call %SONAR_SCANER_BAT% -D"sonar.projectKey=Unified-Cpp" -D"sonar.sources=." -D"sonar.cfamily.build-wrapper-output=bw-output" -D"sonar.host.url=%URL_PATH%" -D"sonar.login=32b01dca3eaa258f830b5fe5edbc46d805fe16be"
echo  "============== END unified-c++ ============="

echo "============= Begin java fronted ============"
cd /d "%JENKINS_PATH_ARCHIVE%\unified\frontend"
call "%SONAR_SCANER_BAT%" -D"sonar.projectKey=Unified-Js-Fronted" -D"sonar.sources=." -D"sonar.host.url=%URL_PATH%" -D"sonar.login=3da59f993e66284195dd334cdfbf4902de1e7f33"
echo  "============= END java fronted ============="

echo "============= Begin java Backend ============"
cd /d "%JENKINS_PATH_ARCHIVE%\unified\backend"
call "%SONAR_SCANER_BAT%" -D"sonar.projectKey=Unified-Js-Backend" -D"sonar.sources=." -D"sonar.host.url=%URL_PATH%" -D"sonar.login=2bd55e628a0207e7abe35f064848c1ca1c739f72"
echo "============== End java Backend ============="

echo "========== Begin embeddedunified-c++========="
rem %BUILD_WRAPER% --out-dir bw-output %DEVNEV% "%JENKINS_PATH_ARCHIVE%\EmbeddedProjectHellowWord\EmbeddedProjectHellowWord.sln" /Rebuild "Release|VisualGDB"
rem call "%SONAR_SCANER_BAT%" -D"sonar.projectKey=Unified-Embedded" -D"sonar.sources=." -D"sonar.cfamily.build-wrapper-output=bw-output" -D"sonar.rem host.url=%URL_PATH%" -D"sonar.login=ff1142fa968e1c6cdea2a8565aec2fa230c2fad2" 
echo "=========== End embeddedunified-c++=========="
