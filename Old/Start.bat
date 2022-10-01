@echo off
python --version
IF %ERRORLEVEL% NEQ 0 GOTO installPython

echo "Do Not Close this window... your outputs will be displayed here. Please continue to check this in case of any issues"

if exist "c:\Program Files\MuseScore 3\bin\MuseScore3.exe" (
    rem file exists
) else (
    echo MuseScore does not exist. This is required to run the program.. redirecting you to install MuseScore.
    echo Rerun the program after installing musescore.
    echo If you need a 32 Bit version, please cancel this installation and start the 32 Bit Installation
    start "" https://musescore.org/en/download
    ..\MuseScore-3.6.2.548021803-x86_64.msi
    pause
)

reg query HKCU\Environment /v PATH 2>NUL |findstr /I "C:.Program.Files.MuseScore.3.bin" 1>NUL
IF %ERRORLEVEL% NEQ 0 GOTO setpath

python Riyaaz.py
IF %ERRORLEVEL% NEQ 0 GOTO setup
exit()


:installPython
echo "You do not have Python on your machine. Please Get and Install"
python 

:setup
echo "Setting up your environment"
pip install pandas
pip install PySimpleGUI
python Riyaaz.py

:setpath
echo "Setting Path. Please Rerun the Program"
setx path "%path%;C:\Program Files\MuseScore 3\bin\"
pause
exit()