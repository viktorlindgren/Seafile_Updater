rmdir /S /Q build
rmdir /S /Q dist
del /Q Seafile Updater Installer.exe

:: Build exe
(python setup.py py2exe || C:\Python27\python setup.py py2exe) || pause

:: Compile installer
("%programfiles(x86)%\Inno Script Studio\ISStudio.exe" -compile "setup.iss" || "%programfiles%\Inno Setup 5\ISCC.exe" /Q "setup.iss" || "%programfiles%\Inno Script Studio\ISStudio.exe" -compile "setup.iss") || "%programfiles%(x86)\Inno Setup 5\ISCC.exe" /Q "setup.iss") || echo. && echo Failed to compile && echo. && pause

:: Clean up
@echo off
rmdir /S /Q build
rmdir /S /Q dist
echo.
echo.
echo Build succeded!
echo.
echo.
pause