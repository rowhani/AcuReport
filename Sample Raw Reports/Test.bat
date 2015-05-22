@echo off

rem ========================================================================
rem
rem "acuReport.bat":  Starter script to run acuReport
rem
rem You may need to adjust
rem
rem       ACUSIM_HOME             - Acusim home directory
rem       ACUSIM_MACHINE          - Machine type
rem       ACUSIM_VERSION          - Release
rem
rem ========================================================================

rem -----------------------------------------------------------------------
rem Get the options
rem -----------------------------------------------------------------------

set opt=
:nextopt
    if "%1"=="" goto end
    set opt=%opt% %1
    shift
    goto nextopt
:end

rem -----------------------------------------------------------------------
rem Basic parameters
rem -----------------------------------------------------------------------

set ACUSIM_HOME=C:\Acusim
set ACUSIM_VERSION=V1.7f
set ACUSIM_MACHINE=WIN
set ACUSIM_ROOT=%ACUSIM_HOME%\%ACUSIM_MACHINE%\%ACUSIM_VERSION%
set ACUSIM_SYSTEM_CNF=%ACUSIM_ROOT%\script\Acusim.cnf
set ACUSIM_CNF_FILES=.\Acusim.cnf:~\Acusim.cnf:%ACUSIM_SYSTEM_CNF%

rem -----------------------------------------------------------------------
rem Set the name
rem -----------------------------------------------------------------------

set ACUSIM_PROG_NAME=acuReport

rem -----------------------------------------------------------------------
rem Get the addresses
rem -----------------------------------------------------------------------

set baseDir=%ACUSIM_ROOT%\base
set libDir=%baseDir%\lib
set binDir=%baseDir%\bin
set scrDir=%ACUSIM_ROOT%\script

rem -----------------------------------------------------------------------
rem Set python path
rem -----------------------------------------------------------------------

set pold=%PATH%
set PATH=%binDir%;%baseDir%\DLLs;%baseDir%\Lib\site-packages;%PATH%
set PATH=%baseDir%\Lib\site-packages\gone;%PATH%
set PATH=%ACUSIM_ROOT%\bin;%PATH%

set PYTHONHOME=%baseDir%
rem set PYTHONPATH=%scrDir%;%binDir% *********

rem -----------------------------------------------------------------------
rem Run acuReport
rem -----------------------------------------------------------------------

set cmd="import sys ; sys.path.insert(0,r'%scrDir%\Report.zip') ; import repMain"

rem %binDir%\python -c %cmd% %opt% *********

%binDir%\python -c "import repMain" -problem HS -file HeatSink.rep -pdf

rem -----------------------------------------------------------------------
rem Reset all
rem -----------------------------------------------------------------------

set PATH=%pold%

set binDir=
set cmd=
set opt=
set panels=
set pold=
set scrDir=
