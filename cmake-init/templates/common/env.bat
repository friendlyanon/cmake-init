@echo off

for /f "tokens=*" %%G in ('"%ProgramFiles(x86)%\Microsoft Visual Studio\Installer\vswhere.exe" -Property InstallationPath') do ^
set "PATH=%PATH%;%%G\Common7\IDE;%cd%\build\dev\Debug"
set "PROMPT=(Debug) %PROMPT%"
