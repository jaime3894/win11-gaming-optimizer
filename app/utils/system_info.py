import platform
import subprocess
import psutil
import winreg


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
    try:
        result = subprocess.run(
            ["wmic", "path", "win32_VideoController", "get", "name"],
            capture_output=True, text=True, timeout=5,
        )
        lines = [l.strip() for l in result.stdout.splitlines() if l.strip() and l.strip().lower() != "name"]
        return lines[0] if lines else "Desconocido"
    except Exception:
        return "Desconocido"


def get_ram_gb() -> float:
    return round(psutil.virtual_memory().total / (1024 ** 3), 1)


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
        return {"total": 0, "free": 0, "percent": 0}


def get_gpu_vendor() -> str:
    name = get_gpu_name().upper()
    if "NVIDIA" in name:
        return "nvidia"
    if "AMD" in name or "RADEON" in name:
        return "amd"
    if "INTEL" in name:
        return "intel"
    return "unknown"


def collect_all() -> dict:
    return {
        "cpu": get_cpu_name(),
        "gpu": get_gpu_name(),
        "gpu_vendor": get_gpu_vendor(),
        "ram_gb": get_ram_gb(),
        "windows": get_windows_version(),
        "disk": get_disk_info(),
        "cpu_cores": psutil.cpu_count(logical=False),
        "cpu_threads": psutil.cpu_count(logical=True),
    }
