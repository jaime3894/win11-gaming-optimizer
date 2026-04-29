"""
Win11 Gaming Optimizer — Entry point.
Auto-eleva privilegios de administrador al iniciar.
"""
import sys
import os


def main():
    # Asegura que el cwd sea la carpeta del script (para imports)
    os.chdir(os.path.dirname(os.path.abspath(__file__)))

    from app.utils.admin import is_admin, elevate

    if not is_admin():
        elevate()
        sys.exit(0)

    try:
        from app.ui.main_window import GamingOptimizerApp
        app = GamingOptimizerApp()
        app.mainloop()
    except Exception:
        import traceback
        with open("error.log", "w", encoding="utf-8") as f:
            f.write(traceback.format_exc())
        raise


if __name__ == "__main__":
    main()
