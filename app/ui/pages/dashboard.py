import customtkinter as ctk
import threading
from app.utils import system_info as si

RISK_COLORS = {"low": "#44ff88", "medium": "#ffaa33", "high": "#ff4444"}

ACCENT = "#e63946"
BG_CARD = "#1a1a2e"
BG_INNER = "#16213e"
TEXT_DIM = "#888899"


class DashboardPage(ctk.CTkFrame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._build_skeleton()
        threading.Thread(target=self._load_info, daemon=True).start()

    def _build_skeleton(self):
        title = ctk.CTkLabel(
            self, text="Dashboard", font=ctk.CTkFont(size=26, weight="bold"),
            text_color="#ffffff",
        )
        title.pack(anchor="w", padx=30, pady=(24, 4))

        subtitle = ctk.CTkLabel(
            self, text="Información del sistema y acceso rápido a optimizaciones",
            font=ctk.CTkFont(size=13), text_color=TEXT_DIM,
        )
        subtitle.pack(anchor="w", padx=30, pady=(0, 20))

        # Info cards grid
        self.cards_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.cards_frame.pack(fill="x", padx=30, pady=(0, 20))

        self.card_labels: dict[str, ctk.CTkLabel] = {}
        specs = [
            ("cpu", "CPU", "Cargando..."),
            ("gpu", "GPU", "Cargando..."),
            ("ram", "RAM", "Cargando..."),
            ("windows", "Windows", "Cargando..."),
            ("disk", "Disco C:", "Cargando..."),
        ]
        for i, (key, title_text, placeholder) in enumerate(specs):
            card = ctk.CTkFrame(self.cards_frame, fg_color=BG_CARD, corner_radius=12)
            card.grid(row=i // 2, column=i % 2, padx=8, pady=8, sticky="ew")
            self.cards_frame.columnconfigure(0, weight=1)
            self.cards_frame.columnconfigure(1, weight=1)

            ctk.CTkLabel(card, text=title_text, font=ctk.CTkFont(size=11, weight="bold"),
                         text_color=ACCENT).pack(anchor="w", padx=16, pady=(12, 2))
            lbl = ctk.CTkLabel(card, text=placeholder, font=ctk.CTkFont(size=13),
                                text_color="#ccccdd", wraplength=320, justify="left")
            lbl.pack(anchor="w", padx=16, pady=(0, 12))
            self.card_labels[key] = lbl

        # Tips section
        tips_frame = ctk.CTkFrame(self, fg_color=BG_CARD, corner_radius=12)
        tips_frame.pack(fill="x", padx=30, pady=(0, 20))

        ctk.CTkLabel(tips_frame, text="Guía rápida",
                     font=ctk.CTkFont(size=14, weight="bold"), text_color=ACCENT,
                     ).pack(anchor="w", padx=16, pady=(14, 6))

        tips = [
            "1. Empieza por la sección Sistema — son las optimizaciones más seguras y efectivas.",
            "2. En Red, el Algoritmo de Nagle es clave para reducir ping en FPS competitivos.",
            "3. La sección Avanzado incluye tweaks de mayor riesgo. Lee cada descripción antes de activar.",
            "4. Usa el botón Restaurar si algo no funciona correctamente después de aplicar.",
        ]
        for tip in tips:
            ctk.CTkLabel(tips_frame, text=tip, font=ctk.CTkFont(size=12),
                         text_color="#aaaacc", wraplength=700, justify="left",
                         ).pack(anchor="w", padx=16, pady=2)
        ctk.CTkLabel(tips_frame, text="").pack(pady=4)

    def _load_info(self):
        try:
            info = si.collect_all()
            disk = info["disk"]
            updates = {
                "cpu": f"{info['cpu']}  ({info['cpu_cores']}C / {info['cpu_threads']}T)" if info['cpu_cores'] else info['cpu'],
                "gpu": info["gpu"],
                "ram": f"{info['ram_gb']} GB" if info['ram_gb'] else "Desconocido",
                "windows": info["windows"],
                "disk": f"{disk['free']:.1f} GB libres de {disk['total']:.1f} GB  ({disk['percent']}% usado)" if disk['total'] else "Desconocido",
            }
        except Exception as e:
            import traceback
            try:
                with open("error.log", "a", encoding="utf-8") as f:
                    f.write("collect_all failed:\n" + traceback.format_exc() + "\n")
            except Exception:
                pass
            updates = {k: "No disponible" for k in self.card_labels.keys()}

        try:
            for key, val in updates.items():
                if key in self.card_labels:
                    lbl = self.card_labels[key]
                    lbl.after(0, lambda l=lbl, v=val: l.configure(text=v))
        except (RuntimeError, Exception):
            pass
