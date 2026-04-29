import platform
import subprocess
import psutil
import winreg

CREATE_NO_WINDOW = 0x08000000


def _run_ps(cmd: str, timeout: int = 8) -> str:
    """Run PowerShell, capture stdout, hide console window (critical for PyInstaller --windowed)."""
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
            capture_output=True,
            text=True,
            timeout=timeout,
            creationflags=CREATE_NO_WINDOW,
        )
        return result.stdout.strip()
    except Exception:
        return ""


def get_cpu_name() -> str:
    try:
        key = winreg.OpenKey(
            winreg.HKEY_LOCAL_MACHINE,
            r"HARDWARE\DESCRIPTION\System\CentralProcessor\0",
        )
        name, _ = winreg.QueryValueEx(key, "ProcessorNameString")
        winreg.CloseKey(key)
        return name.strip()
    except Exception:
        return platform.processor() or "Desconocido"


def get_gpu_name() -> str:
    # Primary: registry walk (no subprocess, fastest)
    try:
        base = r"SYSTEM\CurrentControlSet\Control\Class\{4d36e968-e325-11ce-bfc1-08002be10318}"
        key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, base)
        i = 0
        while True:
            try:
                sub = winreg.EnumKey(key, i)
            except OSError:
                break
            i += 1
            if not sub.isdigit():
                continue
            try:
                sk = winreg.OpenKey(key, sub)
                desc, _ = winreg.QueryValueEx(sk, "DriverDesc")
                winreg.CloseKey(sk)
                if desc and not desc.lower().startswith("microsoft basic"):
                    winreg.CloseKey(key)
                    return desc.strip()
            except Exception:
                continue
        winreg.CloseKey(key)
    except Exception:
        pass

    # Fallback: PowerShell CIM (replaces deprecated wmic)
    out = _run_ps('(Get-CimInstance Win32_VideoController | Select-Object -First 1).Name')
    return out if out else "Desconocido"


def get_ram_gb() -> float:
    try:
        return round(psutil.virtual_memory().total / (1024 ** 3), 1)
    except Exception:
        return 0.0


def get_windows_version() -> str:
    try:
        ver = platform.version()
        release = platform.release()
        return f"Windows {release} ({ver})"
    except Exception:
        return "Windows (desconocido)"


def get_disk_info() -> dict:
    try:
        usage = psutil.disk_usage("C:\\")
        return {
            "total": round(usage.total / (1024 ** 3), 1),
            "free": round(usage.free / (1024 ** 3), 1),
            "percent": usage.percent,
        }
    except Exception:
        return {"total": 0.0, "free": 0.0, "percent": 0}


def collect_all() -> dict:
    cpu = get_cpu_name()
    gpu = get_gpu_name()
    gpu_upper = gpu.upper()
    if "NVIDIA" in gpu_upper:
        vendor = "nvidia"
    elif "AMD" in gpu_upper or "RADEON" in gpu_upper:
        vendor = "amd"
    elif "INTEL" in gpu_upper:
        vendor = "intel"
    else:
        vendor = "unknown"

    try:
        cores = psutil.cpu_count(logical=False) or 0
        threads = psutil.cpu_count(logical=True) or 0
    except Exception:
        cores, threads = 0, 0

    return {
        "cpu": cpu,
        "gpu": gpu,
        "gpu_vendor": vendor,
        "ram_gb": get_ram_gb(),
        "windows": get_windows_version(),
        "disk": get_disk_info(),
        "cpu_cores": cores,
        "cpu_threads": threads,
    }
