@echo off
rem =================================
rem =================================
rem ====== The batch  script  =======
rem =========== Embedded ============
rem === Build by Sergey Yvstigneev ==
rem =================================
rem =================================

set MPLAB_EXE="C:\Program Files (x86)\Microchip\MPLABX\v5.35\mplab_platform\bin\mplab_ide64.exe"
set NuET_RF_Bootloader="F:\jenkins\workspace\LeoPrj\Leo\Embedded\nuera-tight-rf-firmware\firmware_btl\NuET_RF_Bootloader.X"
set MAKE_EXE="C:\Program Files (x86)\Microchip\MPLABX\v5.35\gnuBins\GnuWin64\bin\make.exe"

set PATH=%PATH%;"C:\Program Files (x86)\Microchip\MPLABX\v5.35\gnuBins\GnuWin64\bin"	
set PATH=%PATH%;"C:\Program Files\Microchip\xc32\v2.41\bin"

cd /d %NuET_RF_Bootloader%
rem %MAKE_EXE% -f Makefile CONF=Debug clean
make -f nbproject\Makefile-RE0973_R5_Bootloader.mk SUBPROJECTS= .clean-conf
make -f nbproject\Makefile-RE0973_R5_Bootloader.mk SUBPROJECTS= .build-conf

		
			
