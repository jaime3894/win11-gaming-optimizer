"""
Definitions for all available optimizations.
Each entry has: id, name, description, risk (low/medium/high),
default (bool), apply (list of PS commands), restore (list of PS commands).
"""

OPTIMIZATIONS: dict[str, list[dict]] = {

    "system": [
        {
            "id": "ultimate_power",
            "name": "Plan de Energía: Máximo Rendimiento",
            "description": "Activa el plan Ultimate Performance que elimina microgestión de energía para máxima estabilidad de frecuencia.",
            "risk": "low",
            "default": True,
            "apply": [
                'powercfg -duplicatescheme e9a42b02-d5df-448d-aa00-03f14749eb61 2>$null; powercfg /setactive e9a42b02-d5df-448d-aa00-03f14749eb61',
            ],
            "restore": [
                'powercfg /setactive SCHEME_BALANCED',
            ],
        },
        {
            "id": "disable_sysmain",
            "name": "Deshabilitar SysMain (Superfetch)",
            "description": "SysMain precarga apps en RAM, consumiendo recursos mientras juegas. Deshabilitarlo libera RAM y reduce I/O.",
            "risk": "low",
            "default": True,
            "apply": [
                'Stop-Service -Name SysMain -Force -ErrorAction SilentlyContinue; Set-Service -Name SysMain -StartupType Disabled',
            ],
            "restore": [
                'Set-Service -Name SysMain -StartupType Automatic; Start-Service -Name SysMain -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "disable_wsearch",
            "name": "Deshabilitar Windows Search (Indexación)",
            "description": "El servicio de indexación consume CPU y disco en background. Deshabilitarlo reduce stuttering durante partidas.",
            "risk": "low",
            "default": True,
            "apply": [
                'Stop-Service -Name WSearch -Force -ErrorAction SilentlyContinue; Set-Service -Name WSearch -StartupType Disabled',
            ],
            "restore": [
                'Set-Service -Name WSearch -StartupType Automatic; Start-Service -Name WSearch -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "disable_gamedvr",
            "name": "Deshabilitar Xbox Game Bar / Game DVR",
            "description": "Game DVR graba en segundo plano consumiendo CPU y GPU. Deshabilitarlo puede aportar varios FPS extra.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR" -Name "AppCaptureEnabled" -Value 0 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_Enabled" -Value 0 -Type DWord -Force',
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR")) { New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" -Force }; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" -Name "AllowGameDVR" -Value 0 -Type DWord -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\GameDVR" -Name "AppCaptureEnabled" -Value 1 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_Enabled" -Value 1 -Type DWord -Force',
                'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\GameDVR" -Name "AllowGameDVR" -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "hags",
            "name": "Hardware Accelerated GPU Scheduling (HAGS)",
            "description": "Permite a la GPU gestionar su propia VRAM directamente, reduciendo latencia de frames. Requiere GPU y driver compatibles.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" -Name "HwSchMode" -Value 2 -Type DWord -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\GraphicsDrivers" -Name "HwSchMode" -Value 1 -Type DWord -Force',
            ],
        },
        {
            "id": "visual_effects",
            "name": "Optimizar Efectos Visuales para Rendimiento",
            "description": "Desactiva animaciones, sombras y transparencias de Windows para liberar CPU y GPU en tareas de interfaz.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value 2 -Type DWord -Force',
                '$path = "HKCU:\\Control Panel\\Desktop"; Set-ItemProperty -Path $path -Name "UserPreferencesMask" -Value ([byte[]](0x90,0x12,0x03,0x80,0x10,0x00,0x00,0x00)) -Type Binary -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\VisualEffects" -Name "VisualFXSetting" -Value 0 -Type DWord -Force',
            ],
        },
        {
            "id": "processor_scheduling",
            "name": "Prioridad de CPU a Programas (no background)",
            "description": "Ajusta el quantum de CPU para favorecer programas en primer plano (juegos) sobre servicios en background.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" -Name "Win32PrioritySeparation" -Value 38 -Type DWord -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\PriorityControl" -Name "Win32PrioritySeparation" -Value 2 -Type DWord -Force',
            ],
        },
        {
            "id": "disable_hibernation",
            "name": "Deshabilitar Hibernación",
            "description": "Elimina el archivo hiberfil.sys (varios GB) y libera espacio en disco. No afecta el rendimiento durante juego.",
            "risk": "low",
            "default": False,
            "apply": [
                'powercfg /hibernate off',
            ],
            "restore": [
                'powercfg /hibernate on',
            ],
        },
        {
            "id": "disable_startup_delay",
            "name": "Eliminar Retraso de Inicio de Aplicaciones",
            "description": "Windows retrasa apps de inicio 10 segundos por defecto. Eliminar este retraso acelera el boot.",
            "risk": "low",
            "default": False,
            "apply": [
                'If (!(Test-Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Serialize")) { New-Item -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Serialize" -Force }; Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Serialize" -Name "StartupDelayInMSec" -Value 0 -Type DWord -Force',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\Explorer\\Serialize" -Name "StartupDelayInMSec" -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "disable_tips",
            "name": "Deshabilitar Notificaciones y Tips de Windows",
            "description": "Elimina las sugerencias y notificaciones del sistema que interrumpen durante las sesiones de juego.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SubscribedContent-338389Enabled" -Value 0 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SubscribedContent-353694Enabled" -Value 0 -Type DWord -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SubscribedContent-338389Enabled" -Value 1 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows\\CurrentVersion\\ContentDeliveryManager" -Name "SubscribedContent-353694Enabled" -Value 1 -Type DWord -Force',
            ],
        },
    ],

    "network": [
        {
            "id": "disable_nagle",
            "name": "Deshabilitar Algoritmo de Nagle",
            "description": "Nagle agrupa paquetes pequeños para eficiencia, pero introduce latencia. Deshabilitarlo reduce el ping en juegos online.",
            "risk": "low",
            "default": True,
            "apply": [
                r'$interfaces = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"; foreach ($i in $interfaces) { Set-ItemProperty -Path $i.PSPath -Name "TcpAckFrequency" -Value 1 -Type DWord -Force -ErrorAction SilentlyContinue; Set-ItemProperty -Path $i.PSPath -Name "TCPNoDelay" -Value 1 -Type DWord -Force -ErrorAction SilentlyContinue }',
            ],
            "restore": [
                r'$interfaces = Get-ChildItem "HKLM:\SYSTEM\CurrentControlSet\Services\Tcpip\Parameters\Interfaces"; foreach ($i in $interfaces) { Remove-ItemProperty -Path $i.PSPath -Name "TcpAckFrequency" -ErrorAction SilentlyContinue; Remove-ItemProperty -Path $i.PSPath -Name "TCPNoDelay" -ErrorAction SilentlyContinue }',
            ],
        },
        {
            "id": "disable_net_throttling",
            "name": "Deshabilitar Network Throttling Index",
            "description": "Windows limita el ancho de banda de red cuando reproduce multimedia. Eliminar esta restricción mejora estabilidad de latencia.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" -Name "NetworkThrottlingIndex" -Value 0xFFFFFFFF -Type DWord -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" -Name "NetworkThrottlingIndex" -Value 10 -Type DWord -Force',
            ],
        },
        {
            "id": "dns_cloudflare",
            "name": "DNS: Cloudflare (1.1.1.1)",
            "description": "Cloudflare DNS es el más rápido del mundo según Benchmark. Reduce el tiempo de resolución de nombres en servers de juego.",
            "risk": "medium",
            "default": False,
            "apply": [
                'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ServerAddresses ("1.1.1.1","1.0.0.1") }',
            ],
            "restore": [
                'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ResetServerAddresses }',
            ],
        },
        {
            "id": "dns_google",
            "name": "DNS: Google (8.8.8.8)",
            "description": "DNS de Google con alta disponibilidad y baja latencia global. Buena alternativa a Cloudflare según tu ISP.",
            "risk": "medium",
            "default": False,
            "apply": [
                'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ServerAddresses ("8.8.8.8","8.8.4.4") }',
            ],
            "restore": [
                'Get-NetAdapter | Where-Object {$_.Status -eq "Up"} | ForEach-Object { Set-DnsClientServerAddress -InterfaceIndex $_.InterfaceIndex -ResetServerAddresses }',
            ],
        },
        {
            "id": "qos_gaming",
            "name": "QoS: Máximo Ancho de Banda para Juegos",
            "description": "Por defecto Windows reserva 20% del ancho de banda para el sistema. Esta optimización libera ese 20% para tus juegos.",
            "risk": "low",
            "default": True,
            "apply": [
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched")) { New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" -Force }; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" -Name "NonBestEffortLimit" -Value 0 -Type DWord -Force',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\Psched" -Name "NonBestEffortLimit" -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "system_responsiveness",
            "name": "System Responsiveness para Juegos",
            "description": "Aumenta la prioridad del sistema multimedia. En juegos reduce micro-stutters causados por audio/sistema.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" -Name "SystemResponsiveness" -Value 0 -Type DWord -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile" -Name "SystemResponsiveness" -Value 20 -Type DWord -Force',
            ],
        },
    ],

    "gpu": [
        {
            "id": "disable_fullscreen_opt",
            "name": "Deshabilitar Optimizaciones de Pantalla Completa",
            "description": "Las optimizaciones de pantalla completa de Windows a veces introducen latencia extra. Deshabilitarlas globalmente puede mejorar el input lag.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_DXGIHonorFSEWindowsCompatible" -Value 1 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_FSEBehavior" -Value 2 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_FSEBehaviorMode" -Value 2 -Type DWord -Force',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_DXGIHonorFSEWindowsCompatible" -ErrorAction SilentlyContinue',
                'Remove-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_FSEBehavior" -ErrorAction SilentlyContinue',
                'Remove-ItemProperty -Path "HKCU:\\System\\GameConfigStore" -Name "GameDVR_FSEBehaviorMode" -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "nvidia_low_latency",
            "name": "[NVIDIA] Modo Ultra Low Latency",
            "description": "Activa NVIDIA Reflex / Low Latency Mode via registro. Reduce hasta 33% el input lag en GPUs NVIDIA compatibles.",
            "risk": "low",
            "default": False,
            "apply": [
                'If (!(Test-Path "HKCU:\\SOFTWARE\\NVIDIA Corporation\\Global\\NVTweak")) { New-Item -Path "HKCU:\\SOFTWARE\\NVIDIA Corporation\\Global\\NVTweak" -Force }; Set-ItemProperty -Path "HKCU:\\SOFTWARE\\NVIDIA Corporation\\Global\\NVTweak" -Name "Shim_NVAPI_RLN_allowed" -Value 1 -Type DWord -Force',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\NVIDIA Corporation\\Global\\NVTweak" -Name "Shim_NVAPI_RLN_allowed" -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "gpu_prio",
            "name": "Prioridad de GPU para juegos",
            "description": "Asigna mayor prioridad al scheduler de GPU para procesos de juego, reduciendo frame drops en momentos de alta carga.",
            "risk": "low",
            "default": True,
            "apply": [
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games")) { New-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games" -Force }',
                '$gp = "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games"; Set-ItemProperty -Path $gp -Name "GPU Priority" -Value 8 -Type DWord -Force; Set-ItemProperty -Path $gp -Name "Priority" -Value 6 -Type DWord -Force; Set-ItemProperty -Path $gp -Name "Scheduling Category" -Value "High" -Type String -Force; Set-ItemProperty -Path $gp -Name "SFIO Priority" -Value "High" -Type String -Force',
            ],
            "restore": [
                '$gp = "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Multimedia\\SystemProfile\\Tasks\\Games"; Set-ItemProperty -Path $gp -Name "GPU Priority" -Value 8 -Type DWord -Force; Set-ItemProperty -Path $gp -Name "Priority" -Value 2 -Type DWord -Force',
            ],
        },
        {
            "id": "mpo_disable",
            "name": "Deshabilitar MPO (Multiplane Overlay)",
            "description": "MPO puede causar pantallazos negros y stuttering en algunas GPUs NVIDIA. Deshabilitarlo resuelve estos problemas.",
            "risk": "medium",
            "default": False,
            "apply": [
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\Dwm")) { New-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\Dwm" -Force }; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\Dwm" -Name "OverlayTestMode" -Value 5 -Type DWord -Force',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows\\Dwm" -Name "OverlayTestMode" -ErrorAction SilentlyContinue',
            ],
        },
    ],

    "games": [
        {
            "id": "fortnite_priority",
            "name": "Fortnite: Alta Prioridad de CPU",
            "description": "Configura FortniteClient-Win64-Shipping para ejecutarse con prioridad Alta en el planificador de Windows.",
            "risk": "low",
            "default": False,
            "apply": [
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\FortniteClient-Win64-Shipping.exe\\PerfOptions")) { New-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\FortniteClient-Win64-Shipping.exe\\PerfOptions" -Force }; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\FortniteClient-Win64-Shipping.exe\\PerfOptions" -Name "CpuPriorityClass" -Value 3 -Type DWord -Force',
            ],
            "restore": [
                'Remove-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\FortniteClient-Win64-Shipping.exe" -Recurse -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "fortnite_disable_fullscreen_opt",
            "name": "Fortnite: Deshabilitar Opt. Pantalla Completa",
            "description": "Desactiva la capa de compatibilidad de pantalla completa específicamente para Fortnite, reduciendo latencia de input.",
            "risk": "low",
            "default": False,
            "apply": [
                'If (!(Test-Path "HKCU:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers")) { New-Item -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers" -Force }',
                '$paths = @("$env:LOCALAPPDATA\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping.exe", "$env:LOCALAPPDATA\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping_EAC.exe"); foreach ($p in $paths) { if (Test-Path $p) { Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers" -Name $p -Value "~ DISABLEDXMAXIMIZEDWINDOWEDMODE" -Type String -Force } }',
            ],
            "restore": [
                '$paths = @("$env:LOCALAPPDATA\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping.exe", "$env:LOCALAPPDATA\\FortniteGame\\Binaries\\Win64\\FortniteClient-Win64-Shipping_EAC.exe"); foreach ($p in $paths) { Remove-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\AppCompatFlags\\Layers" -Name $p -ErrorAction SilentlyContinue }',
            ],
        },
        {
            "id": "valorant_priority",
            "name": "Valorant: Alta Prioridad de CPU",
            "description": "Configura VALORANT-Win64-Shipping para ejecutarse con prioridad Alta, especialmente útil en CPUs de pocos núcleos.",
            "risk": "low",
            "default": False,
            "apply": [
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\VALORANT-Win64-Shipping.exe\\PerfOptions")) { New-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\VALORANT-Win64-Shipping.exe\\PerfOptions" -Force }; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\VALORANT-Win64-Shipping.exe\\PerfOptions" -Name "CpuPriorityClass" -Value 3 -Type DWord -Force',
            ],
            "restore": [
                'Remove-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\VALORANT-Win64-Shipping.exe" -Recurse -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "cs2_priority",
            "name": "CS2: Alta Prioridad de CPU",
            "description": "Configura cs2.exe para ejecutarse con prioridad Alta. En CS2, especialmente útil para mantener FPS estables.",
            "risk": "low",
            "default": False,
            "apply": [
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\cs2.exe\\PerfOptions")) { New-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\cs2.exe\\PerfOptions" -Force }; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\cs2.exe\\PerfOptions" -Name "CpuPriorityClass" -Value 3 -Type DWord -Force',
            ],
            "restore": [
                'Remove-Item -Path "HKLM:\\SOFTWARE\\Microsoft\\Windows NT\\CurrentVersion\\Image File Execution Options\\cs2.exe" -Recurse -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "game_mode",
            "name": "Activar Windows Game Mode",
            "description": "Game Mode de Windows 11 asigna más recursos de CPU/GPU al juego activo y suspende tareas de background.",
            "risk": "low",
            "default": True,
            "apply": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\GameBar" -Name "AutoGameModeEnabled" -Value 1 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\GameBar" -Name "AllowAutoGameMode" -Value 1 -Type DWord -Force',
            ],
            "restore": [
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\GameBar" -Name "AutoGameModeEnabled" -Value 0 -Type DWord -Force',
                'Set-ItemProperty -Path "HKCU:\\SOFTWARE\\Microsoft\\GameBar" -Name "AllowAutoGameMode" -Value 0 -Type DWord -Force',
            ],
        },
    ],

    "advanced": [
        {
            "id": "disable_spectre_meltdown",
            "name": "Deshabilitar Mitigaciones Spectre/Meltdown",
            "description": "Las mitigaciones de seguridad para Spectre/Meltdown reducen el rendimiento de CPU hasta un 10-30%. Solo desactivar en PCs que NO se usan para banca/trabajo sensible.",
            "risk": "high",
            "default": False,
            "apply": [
                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" -Name "FeatureSettingsOverride" -Value 3 -Type DWord -Force',
                'Set-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" -Name "FeatureSettingsOverrideMask" -Value 3 -Type DWord -Force',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" -Name "FeatureSettingsOverride" -ErrorAction SilentlyContinue',
                'Remove-ItemProperty -Path "HKLM:\\SYSTEM\\CurrentControlSet\\Control\\Session Manager\\Memory Management" -Name "FeatureSettingsOverrideMask" -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "disable_core_parking",
            "name": "Deshabilitar Core Parking",
            "description": "Windows aparca núcleos de CPU en reposo para ahorrar energía. Deshabilitarlo garantiza que todos los núcleos estén disponibles instantáneamente.",
            "risk": "low",
            "default": True,
            "apply": [
                'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR CPMINCORES 100; powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR CPMAXCORES 100; powercfg /setactive SCHEME_CURRENT',
            ],
            "restore": [
                'powercfg /setacvalueindex SCHEME_CURRENT SUB_PROCESSOR CPMINCORES 0; powercfg /setactive SCHEME_CURRENT',
            ],
        },
        {
            "id": "disable_win_update_p2p",
            "name": "Deshabilitar Windows Update P2P (Optimización de Entrega)",
            "description": "Impide que Windows comparta actualizaciones con otras PCs de Internet usando tu ancho de banda durante el juego.",
            "risk": "low",
            "default": True,
            "apply": [
                'If (!(Test-Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization")) { New-Item -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" -Force }; Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" -Name "DODownloadMode" -Value 0 -Type DWord -Force',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DeliveryOptimization" -Name "DODownloadMode" -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "disable_telemetry",
            "name": "Reducir Telemetría de Windows",
            "description": "Reduce la recopilación de datos de diagnóstico al mínimo. Libera ciclos de CPU/red usados por el proceso de diagnóstico.",
            "risk": "low",
            "default": False,
            "apply": [
                'Set-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -Value 0 -Type DWord -Force',
                'Stop-Service -Name DiagTrack -Force -ErrorAction SilentlyContinue; Set-Service -Name DiagTrack -StartupType Disabled -ErrorAction SilentlyContinue',
            ],
            "restore": [
                'Remove-ItemProperty -Path "HKLM:\\SOFTWARE\\Policies\\Microsoft\\Windows\\DataCollection" -Name "AllowTelemetry" -ErrorAction SilentlyContinue',
                'Set-Service -Name DiagTrack -StartupType Automatic -ErrorAction SilentlyContinue; Start-Service -Name DiagTrack -ErrorAction SilentlyContinue',
            ],
        },
        {
            "id": "irq_priority_gpu",
            "name": "Prioridad IRQ para GPU",
            "description": "Eleva la prioridad de interrupción de la GPU en el bus PCI. Puede reducir frame pacing en escenas de alta carga.",
            "risk": "medium",
            "default": False,
            "apply": [
                '$gpu = Get-PnpDevice | Where-Object {$_.Class -eq "Display" -and $_.Status -eq "OK"} | Select-Object -First 1; if ($gpu) { $devPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\" + $gpu.InstanceId + "\\Device Parameters\\Interrupt Management\\Affinity Policy"; If (!(Test-Path $devPath)) { New-Item -Path $devPath -Force }; Set-ItemProperty -Path $devPath -Name "DevicePriority" -Value 2 -Type DWord -Force }',
            ],
            "restore": [
                '$gpu = Get-PnpDevice | Where-Object {$_.Class -eq "Display" -and $_.Status -eq "OK"} | Select-Object -First 1; if ($gpu) { $devPath = "HKLM:\\SYSTEM\\CurrentControlSet\\Enum\\" + $gpu.InstanceId + "\\Device Parameters\\Interrupt Management\\Affinity Policy"; Remove-ItemProperty -Path $devPath -Name "DevicePriority" -ErrorAction SilentlyContinue }',
            ],
        },
    ],
}
