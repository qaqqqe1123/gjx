#define MyAppName "系统工具箱"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Same0ld"
#define MyAppURL "https://github.com/Same0ld"
#define MyAppExeName "system_toolbox.exe"

[Setup]
; 注: AppId的值为单独标识该应用程序。
; 不要为其他安装程序使用相同的AppId值。
; (若要生成新的 GUID，可在菜单中点击 "工具|生成 GUID")
AppId={{A1234567-B123-C123-D123-E1234567890F}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}
AllowNoIcons=yes
; 需要管理员权限
PrivilegesRequired=admin
OutputDir=output
OutputBaseFilename=系统工具箱_setup
; 移除图标设置，使用默认图标
;SetupIconFile=assets\icon.ico
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern
; 禁用安装目录选择页面的"浏览"按钮
DisableDirPage=auto
; 禁用开始菜单文件夹选择页面
DisableProgramGroupPage=yes
; 安装程序将不允许安装在包含非ASCII字符的路径下
AllowUNCPath=false
; 显示安装详细信息
ShowLanguageDialog=no
VersionInfoVersion={#MyAppVersion}
VersionInfoCompany={#MyAppPublisher}
VersionInfoCopyright=Copyright (C) 2024 {#MyAppPublisher}
VersionInfoProductName={#MyAppName}
VersionInfoProductVersion={#MyAppVersion}
UninstallDisplayName={#MyAppName}
SetupLogging=yes

[Languages]
Name: "chinesesimplified"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 6.1; Check: not IsAdminInstallMode

[Files]
Source: "dist\system_toolbox\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "dist\system_toolbox\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs
; 注意: 不要在任何共享系统文件上使用"Flags: ignoreversion"

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent

[Code]
function InitializeSetup(): Boolean;
begin
  Result := True;
  
  if not IsAdmin then
  begin
    MsgBox('安装程序需要管理员权限才能继续。请以管理员身份运行安装程序。', mbError, MB_OK);
    Result := False;
    Exit;
  end;
  
  if CheckForMutexes('{#MyAppName}_Installation_Mutex') then
  begin
    MsgBox('另一个安装实例正在运行。请先完成或取消该安装。', mbError, MB_OK);
    Result := False;
    Exit;
  end;
  
  CreateMutex('{#MyAppName}_Installation_Mutex');
end;

[UninstallDelete]
Type: filesandordirs; Name: "{app}"

[CustomMessages]
chinesesimplified.InstallingService=正在安装系统服务...
chinesesimplified.UninstallingService=正在卸载系统服务... 