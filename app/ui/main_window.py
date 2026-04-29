import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

from app.utils.admin import is_admin
from app.optimizations.runner import apply_optimizations

from app.ui.pages.dashboard import DashboardPage
from app.ui.pages.system_page import SystemPage
from app.ui.pages.network_page import NetworkPage
from app.ui.pages.gpu_page import GpuPage
from app.ui.pages.games_page import GamesPage
from app.ui.pages.advanced_page import AdvancedPage

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

ACCENT = "#e63946"
ACCENT_HOVER = "#c62333"
BG_MAIN = "#0f0f1a"
BG_SIDEBAR = "#0a0a14"
BG_CARD = "#1a1a2e"
TEXT_DIM = "#888899"

LOG_COLORS = {
    "info":  "#88aaff",
    "ok":    "#44ff88",
    "warn":  "#ffaa33",
    "error": "#ff4466",
}


class GamingOptimizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Win11 Gaming Optimizer")
        self.geometry("1200x720")
        self.minsize(1000, 640)
        self.configure(fg_color=BG_MAIN)

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self._pages: dict[str, ctk.CTkFrame] = {}
        self._nav_buttons: dict[str, ctk.CTkButton] = {}
        self._current_page: str | None = None
        self._log_visible = False
        self._busy = False

        self._build_sidebar()
        self._build_main_area()
        self._build_log_panel()
        self._build_pages()

        self._show_page("dashboard")

    # ---------- UI Construction ----------

    def _build_sidebar(self):
        sb = ctk.CTkFrame(self, fg_color=BG_SIDEBAR, corner_radius=0, width=230)
        sb.grid(row=0, column=0, rowspan=2, sticky="ns")
        sb.grid_propagate(False)

        # Logo
        logo_frame = ctk.CTkFrame(sb, fg_color="transparent")
        logo_frame.pack(fill="x", padx=20, pady=(24, 6))

        ctk.CTkLabel(logo_frame, text="WIN11", font=ctk.CTkFont(size=18, weight="bold"),
                     text_color=ACCENT).pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="Gaming Optimizer",
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#ffffff",
                     ).pack(anchor="w")
        ctk.CTkLabel(logo_frame, text="v1.0", font=ctk.CTkFont(size=10),
                     text_color=TEXT_DIM).pack(anchor="w")

        # Admin badge
        admin_status = "● Admin" if is_admin() else "○ Sin Admin"
        admin_color = "#44ff88" if is_admin() else "#ff4466"
        ctk.CTkLabel(sb, text=admin_status, font=ctk.CTkFont(size=11, weight="bold"),
                     text_color=admin_color).pack(anchor="w", padx=22, pady=(8, 18))

        # Separator
        ctk.CTkFrame(sb, fg_color="#1a1a2e", height=1).pack(fill="x", padx=16, pady=(0, 14))

        # Nav
        nav_items = [
            ("dashboard", "  Dashboard"),
            ("system",    "  Sistema"),
            ("network",   "  Red"),
            ("gpu",       "  GPU"),
            ("games",     "  Juegos"),
            ("advanced",  "  Avanzado"),
        ]
        for key, label in nav_items:
            btn = ctk.CTkButton(
                sb, text=label, anchor="w", height=38,
                font=ctk.CTkFont(size=13),
                fg_color="transparent", hover_color="#1a1a2e",
                text_color="#ccccdd", corner_radius=6,
                command=lambda k=key: self._show_page(k),
            )
            btn.pack(fill="x", padx=12, pady=2)
            self._nav_buttons[key] = btn

        # Bottom action buttons
        spacer = ctk.CTkFrame(sb, fg_color="transparent")
        spacer.pack(fill="both", expand=True)

        actions = ctk.CTkFrame(sb, fg_color="transparent")
        actions.pack(fill="x", side="bottom", padx=14, pady=14)

        self.apply_btn = ctk.CTkButton(
            actions, text="✓ Aplicar Selección", height=42,
            font=ctk.CTkFont(size=13, weight="bold"),
            fg_color=ACCENT, hover_color=ACCENT_HOVER, text_color="#ffffff",
            command=self._on_apply,
        )
        self.apply_btn.pack(fill="x", pady=(0, 6))

        self.restore_btn = ctk.CTkButton(
            actions, text="↺ Restaurar", height=34,
            font=ctk.CTkFont(size=12),
            fg_color="#2a2a4a", hover_color="#3a3a6a", text_color="#ccccff",
            command=self._on_restore,
        )
        self.restore_btn.pack(fill="x", pady=(0, 6))

        self.log_toggle = ctk.CTkButton(
            actions, text="▼ Mostrar Log", height=28,
            font=ctk.CTkFont(size=11),
            fg_color="transparent", hover_color="#1a1a2e", text_color=TEXT_DIM,
            command=self._toggle_log,
        )
        self.log_toggle.pack(fill="x")

    def _build_main_area(self):
        self.main_area = ctk.CTkFrame(self, fg_color=BG_MAIN, corner_radius=0)
        self.main_area.grid(row=0, column=1, sticky="nsew")
        self.main_area.grid_columnconfigure(0, weight=1)
        self.main_area.grid_rowconfigure(0, weight=1)

    def _build_log_panel(self):
        self.log_frame = ctk.CTkFrame(self, fg_color="#08080f", corner_radius=0, height=180)
        # Built but not gridded yet (toggle)

        header = ctk.CTkFrame(self.log_frame, fg_color="#08080f")
        header.pack(fill="x", padx=14, pady=(8, 4))

        ctk.CTkLabel(header, text="LOG DE ACTIVIDAD",
                     font=ctk.CTkFont(size=11, weight="bold"), text_color=ACCENT,
                     ).pack(side="left")

        ctk.CTkButton(header, text="Limpiar", width=80, height=22,
                      font=ctk.CTkFont(size=10),
                      fg_color="#1a1a2e", hover_color="#2a2a4a", text_color=TEXT_DIM,
                      command=self._clear_log,
                      ).pack(side="right")

        self.log_box = ctk.CTkTextbox(
            self.log_frame, fg_color="#050508", text_color="#cccccc",
            font=ctk.CTkFont(family="Consolas", size=11), wrap="word",
        )
        self.log_box.pack(fill="both", expand=True, padx=14, pady=(0, 10))
        self.log_box.configure(state="disabled")

        for tag, color in LOG_COLORS.items():
            self.log_box.tag_config(tag, foreground=color)

    def _build_pages(self):
        self._pages["dashboard"] = DashboardPage(self.main_area)
        self._pages["system"]    = SystemPage(self.main_area)
        self._pages["network"]   = NetworkPage(self.main_area)
        self._pages["gpu"]       = GpuPage(self.main_area)
        self._pages["games"]     = GamesPage(self.main_area)
        self._pages["advanced"]  = AdvancedPage(self.main_area)

        for page in self._pages.values():
            page.grid(row=0, column=0, sticky="nsew")
            page.grid_remove()

    # ---------- Navigation ----------

    def _show_page(self, key: str):
        if self._current_page == key:
            return
        if self._current_page:
            self._pages[self._current_page].grid_remove()
            self._nav_buttons[self._current_page].configure(
                fg_color="transparent", text_color="#ccccdd",
            )

        self._pages[key].grid()
        self._nav_buttons[key].configure(fg_color="#1a1a2e", text_color=ACCENT)
        self._current_page = key

    # ---------- Apply / Restore ----------

    def _get_current_selection(self) -> list[dict]:
        page = self._pages.get(self._current_page)
        if hasattr(page, "get_selected_opts"):
            return page.get_selected_opts()
        return []

    def _on_apply(self):
        if self._busy:
            return
        if self._current_page in ("dashboard",):
            messagebox.showinfo(
                "Selecciona una categoría",
                "Ve a Sistema, Red, GPU, Juegos o Avanzado y elige las optimizaciones que quieres aplicar.",
            )
            return

        selected = self._get_current_selection()
        if not selected:
            messagebox.showinfo(
                "Sin selección",
                "No has seleccionado ninguna optimización en esta categoría.",
            )
            return

        msg = f"Vas a aplicar {len(selected)} optimización(es). ¿Continuar?\n\n"
        msg += "\n".join(f"• {o['name']}" for o in selected[:8])
        if len(selected) > 8:
            msg += f"\n... y {len(selected) - 8} más"

        if not messagebox.askyesno("Confirmar aplicación", msg):
            return

        self._run("apply", selected)

    def _on_restore(self):
        if self._busy:
            return
        if self._current_page in ("dashboard",):
            messagebox.showinfo(
                "Selecciona una categoría",
                "Ve a una categoría y selecciona las optimizaciones que quieres revertir.",
            )
            return

        selected = self._get_current_selection()
        if not selected:
            messagebox.showinfo(
                "Sin selección",
                "Selecciona las optimizaciones a revertir.",
            )
            return

        if not messagebox.askyesno(
            "Confirmar restauración",
            f"Vas a revertir {len(selected)} optimización(es) a sus valores por defecto. ¿Continuar?",
        ):
            return

        self._run("restore", selected)

    def _run(self, mode: str, opts: list[dict]):
        self._busy = True
        self.apply_btn.configure(state="disabled", text="Procesando...")
        self.restore_btn.configure(state="disabled")
        if not self._log_visible:
            self._toggle_log()

        action = "APLICAR" if mode == "apply" else "RESTAURAR"
        self._log("info", f"━━━ {action} {len(opts)} optimización(es) ━━━")

        apply_optimizations(opts, self._log, self._on_done, mode=mode)

    def _on_done(self, success: int, fail: int):
        def _finish():
            self._busy = False
            self.apply_btn.configure(state="normal", text="✓ Aplicar Selección")
            self.restore_btn.configure(state="normal")
            self._log("info", f"━━━ FIN: {success} OK, {fail} con errores ━━━")
            if fail == 0:
                self._log("ok", "Todas las optimizaciones se aplicaron correctamente.")
            else:
                self._log("warn", f"{fail} optimización(es) fallaron. Revisa el log.")
            self._log("info", "ⓘ Algunos cambios requieren reiniciar Windows para tener efecto completo.")

        self.after(0, _finish)

    # ---------- Log ----------

    def _toggle_log(self):
        if self._log_visible:
            self.log_frame.grid_forget()
            self.log_toggle.configure(text="▼ Mostrar Log")
            self._log_visible = False
            self.grid_rowconfigure(1, weight=0)
        else:
            self.log_frame.grid(row=1, column=1, sticky="ew")
            self.log_toggle.configure(text="▲ Ocultar Log")
            self._log_visible = True

    def _log(self, level: str, msg: str):
        def _do():
            ts = datetime.now().strftime("%H:%M:%S")
            self.log_box.configure(state="normal")
            self.log_box.insert("end", f"[{ts}] ", "info")
            self.log_box.insert("end", f"{msg}\n", level)
            self.log_box.see("end")
            self.log_box.configure(state="disabled")
        self.after(0, _do)

    def _clear_log(self):
        self.log_box.configure(state="normal")
        self.log_box.delete("1.0", "end")
        self.log_box.configure(state="disabled")
