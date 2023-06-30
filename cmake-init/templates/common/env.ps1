$oldPrompt = (Get-Command prompt).ScriptBlock

function prompt() { "(Debug) $(& $oldPrompt)" }

$VsInstallPath = & "${env:ProgramFiles(x86)}\Microsoft Visual Studio\Installer\vswhere.exe" -Property InstallationPath
$Env:Path += ";$VsInstallPath\Common7\IDE;$Pwd\build\dev\Debug"
