; Script Reparado - SaoPdfxlxx Enterprise
; Solución al error "CreateProcess failed; code 2"

#define MyAppName "SaoPdfxlxx Enterprise"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Sao Systems"
#define MyAppExeName "SaoPdfxlxx.exe"

[Setup]
; --- Identidad ---
AppId={{A2F9A3C1-E8B2-45D6-98F1-SAO_SYSTEMS_FIX}}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\{#MyAppName}
DefaultGroupName={#MyAppName}

; --- Configuración Técnica ---
; PrivilegesRequired=lowest permite instalar sin ser admin (evita bloqueos de Windows)
PrivilegesRequired=lowest
OutputDir=Installers
OutputBaseFilename=Instalador_SaoPdfxlxx_v1.0_Final
Compression=lzma2/ultra64
SolidCompression=yes
WizardStyle=modern

; --- Iconos ---
SetupIconFile=assets\mi_logo.ico
UninstallDisplayIcon={app}\{#MyAppExeName}

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked

[Files]
; --- CRÍTICO: AQUÍ ESTABA EL ERROR ---
; Source debe apuntar a la carpeta que contiene el .exe
; El asterisco (*) copia TODO el contenido de esa carpeta a la carpeta de instalación {app}
Source: "C:\Users\Display\OneDrive\ProyectosGrandes\Saopdfxlxx\dist\SaoPdfxlxx/*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs createallsubdirs

Source: "README.md"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{group}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon

[Run]
; Aquí es donde fallaba antes. Ahora que aseguramos el nombre en el Paso 2, funcionará.
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{#StringChange(MyAppName, '&', '&&')}}"; Flags: nowait postinstall skipifsilent