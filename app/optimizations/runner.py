import subprocess
import threading
from typing import Callable


def _run_ps(command: str) -> tuple[bool, str]:
    try:
        result = subprocess.run(
            ["powershell", "-NoProfile", "-NonInteractive", "-ExecutionPolicy", "Bypass", "-Command", command],
            capture_output=True, text=True, timeout=30,
        )
        if result.returncode != 0 and result.stderr.strip():
            return False, result.stderr.strip()
        return True, result.stdout.strip()
    except subprocess.TimeoutExpired:
        return False, "Timeout: el comando tardó más de 30 segundos"
    except Exception as e:
        return False, str(e)


def apply_optimizations(
    opts: list[dict],
    log_callback: Callable[[str, str], None],
    done_callback: Callable[[int, int], None],
    mode: str = "apply",
):
    """Run in a separate thread. mode = 'apply' | 'restore'"""

    def _worker():
        success = 0
        fail = 0
        key = "apply" if mode == "apply" else "restore"

        for opt in opts:
            name = opt["name"]
            log_callback("info", f"▶  {name}...")
            commands = opt.get(key, [])
            if not commands:
                log_callback("warn", f"   Sin comandos para '{name}', omitiendo.")
                continue

            all_ok = True
            for cmd in commands:
                ok, msg = _run_ps(cmd)
                if not ok:
                    log_callback("error", f"   ✗ Error: {msg}")
                    all_ok = False
                    break

            if all_ok:
                log_callback("ok", f"   ✔ Completado")
                success += 1
            else:
                fail += 1

        done_callback(success, fail)

    t = threading.Thread(target=_worker, daemon=True)
    t.start()
