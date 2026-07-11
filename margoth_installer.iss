[Setup]
AppName=Margoth
AppVersion=1.1.0
AppVerName=Margoth 1.1.0
AppPublisher=Carlos G
AppComments=Rehabilitación cognitiva y del lenguaje, 100% offline
DefaultDirName={localappdata}\Margoth
DefaultGroupName=Margoth
OutputBaseFilename=Margoth_Setup
OutputDir=dist
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
SetupIconFile=assets\icon.ico
UninstallDisplayIcon={app}\Margoth.exe
ArchitecturesInstallIn64BitMode=x64compatible

[Dirs]
Name: "{app}"; Permissions: users-modify

[Files]
Source: "dist\Margoth\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

[Icons]
Name: "{autodesktop}\Margoth"; Filename: "{app}\Margoth.exe"
Name: "{group}\Margoth"; Filename: "{app}\Margoth.exe"

[Run]
Filename: "{app}\Margoth.exe"; Description: "Iniciar Margoth"; Flags: nowait postinstall skipifsilent
