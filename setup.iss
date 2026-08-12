; Inno Setup Script for WebP Converter Pro
#define MyAppName "WebP Converter Pro"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Suraj Kumar (miniOrange)"
#define MyAppExeName "WebP Converter Pro.exe"

[Setup]
AppId={{D37F8A2E-9C8B-4B21-8F12-881234567890}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={userappdata}\Programs\{#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=WebP_Converter_Pro_Setup
Compression=lzma2/max
SolidCompression=yes
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\{#MyAppExeName}
PrivilegesRequired=lowest

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"

[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion uninsrestartdelete

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent
