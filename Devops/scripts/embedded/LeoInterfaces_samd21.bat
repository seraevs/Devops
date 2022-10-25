@echo off
rem =================================
rem =================================
rem ====== The batch  script  =======
rem =========== Embedded ============
rem === Build by Sergey Yvstigneev ==
rem =================================
rem =================================

set MPLAB_EXE="C:\Program Files (x86)\Microchip\MPLABX\v5.35\mplab_platform\bin\mplab_ide64.exe"
set LeoInterfaces="F:\jenkins\workspace\LeoPrj\Leo\Embedded\HP_Interface\apps\device\cdc_com_port_single\firmware\LeoInterfaces_samd21.X"
set MAKE_EXE="C:\Program Files (x86)\Microchip\MPLABX\v5.35\gnuBins\GnuWin64\bin\make.exe"

set PATH=%PATH%;"C:\Program Files (x86)\Microchip\MPLABX\v5.35\gnuBins\GnuWin64\bin"	
set PATH=%PATH%;"C:\Program Files\Microchip\xc32\v2.41\bin"

cd /d %LeoInterfaces%
rem %MAKE_EXE% -f Makefile CONF=Debug clean
make -f nbproject/Makefile-Config_G18A_Dbg.mk SUBPROJECTS= .clean-conf
make -f nbproject/Makefile-Config_G18A_Dbg.mk SUBPROJECTS= .build-conf
