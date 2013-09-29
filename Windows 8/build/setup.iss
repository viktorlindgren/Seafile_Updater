[Setup]
AppId={{6D49D8DA-82FB-411B-895A-3082F92D3CA2}
AppName=Seafile Updater
AppVersion=1.2
AppPublisher=Viktor Lindgren
DefaultDirName={pf}\Seafile Updater
DefaultGroupName=Seafile Updater
OutputBaseFilename=Seafile Updater Installer
Compression=lzma
SolidCompression=yes
OutputDir="."
PrivilegesRequired=admin


DisableWelcomePage=yes
DisableDirPage=yes
DisableProgramGroupPage=yes
DisableReadyMemo=yes
DisableReadyPage=yes
DisableStartupPrompt=yes
DisableFinishedPage=yes

; Stop old process when installing

[Code]
procedure CurStepChanged(CurStep: TSetupStep);
var ResultCode: integer;
begin
	if CurStep = ssInstall then
	begin
    if Exec(ExpandConstant('taskkill.exe'), '/F /im Check4SeafileUpdate.exe', '',
          SW_HIDE, ewWaitUntilTerminated, ResultCode) then
    begin
      // Everything went fine
    end
    else begin
        msgbox('Could not overwrite existing installation, please uninstall before installing', mbError, MB_OK)
        SysErrorMessage(ResultCode)
    end
  end;
end;

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "dist\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{userstartup}\Seafile Updater"; Filename: "{app}\StartChecker.vbs"

[Run]
Filename: "{app}\Check4SeafileUpdate.exe"; Flags: nowait shellexec postinstall runascurrentuser; Description: "{cm:LaunchProgram,Seafile Updater}"

[UninstallRun]
Filename: "taskkill"; Parameters: "/F /im Check4SeafileUpdate.exe"; Flags: runhidden shellexec waituntilterminated
