[Setup]
AppName=Margoth
AppVersion=1.0.0
DefaultDirName={localappdata}\Margoth
DefaultGroupName=Margoth
OutputBaseFilename=Margoth_Setup
OutputDir=dist
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
UninstallDisplayIcon={app}\Margoth.exe
ArchitecturesInstallIn64BitMode=x64

[Dirs]
Name: "{app}"; Permissions: users-modify

[Files]
Source: "dist\Margoth\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\Margoth"; Filename: "{app}\Margoth.exe"
Name: "{group}\Margoth"; Filename: "{app}\Margoth.exe"

[Run]
Filename: "{app}\Margoth.exe"; Description: "Iniciar Margoth"; Flags: nowait postinstall skipifsilent
