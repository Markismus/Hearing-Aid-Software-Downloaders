@echo off

echo DISCLAIMER
echo I (Bluebotlabz), do not take any responsability for what you do using this software
echo All rights and credit go to their rightful owners. No copyright infringement intended.
echo.
echo Bluebotlabz and this downloader are not affiliated with or endorsed by any of the companies mentioned in this repository
echo Depending on how this software is used, it may breach the EULA of the downloaded software
echo This is an UNOFFICIAL downloader and use of the software downloaded using it may be limited

echo.
echo.
echo.

echo Installing requirements...
pip3 install -r ./requirements.txt


:Menu
echo.
echo.

echo Hearing Aid Software downloader
echo 1) Phonak Target Downloader
echo 2) Signia Connexx Downloader

echo.
set /p SELECTION="Please choose a downloader to run: "

IF %SELECTION%==1 ( python "./Phonak Target Downloader.py" & GOTO Finished )
IF %SELECTION%==2 ( python "./Signia Connexx Downloader.py" & GOTO Finished )

echo Invalid selection made, please try again
pause
GOTO Menu


:Finished
pause