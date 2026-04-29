"""
Shared base for optimization pages — renders a scrollable list of toggle cards.
"""
import customtkinter as ctk
from typing import Callable

ACCENT = "#e63946"
BG_CARD = "#1a1a2e"
BG_INNER = "#16213e"
TEXT_DIM = "#888899"

RISK_MAP = {
    "low":    ("#1a3a2a", "#44ff88", "BAJO"),
    "medium": ("#3a2a10", "#ffaa33", "MEDIO"),
    "high":   ("#3a1010", "#ff4444", "ALTO"),
}


class OptimizationPage(ctk.CTkFrame):
    """Generic page that renders a list of optimizations with toggle switches."""

    def __init__(
        self,
        parent,
        title: str,
        description: str,
        optimizations: list[dict],
        get_selected_callback: Callable[[], dict],
        **kwargs,
    ):
        super().__init__(parent, fg_color="transparent", **kwargs)
        self._opts = optimizations
        self._switches: dict[str, ctk.CTkSwitch] = {}
        self._vars: dict[str, ctk.BooleanVar] = {}
        self._get_selected = get_selected_callback

        self._build(title, description)

    def _build(self, title: str, description: str):
        # Header
        ctk.CTkLabel(self, text=title,
                     font=ctk.CTkFont(size=26, weight="bold"), text_color="#ffffff",
                     ).pack(anchor="w", padx=30, pady=(24, 4))
        ctk.CTkLabel(self, text=description,
                     font=ctk.CTkFont(size=13), text_color=TEXT_DIM,
                     ).pack(anchor="w", padx=30, pady=(0, 6))

        # Select-all row
        top_bar = ctk.CTkFrame(self, fg_color="transparent")
        top_bar.pack(fill="x", padx=30, pady=(0, 12))
        ctk.CTkButton(top_bar, text="Seleccionar todo", width=130, height=28,
                      fg_color="#2a2a4a", hover_color="#3a3a6a", text_color="#ccccff",
                      font=ctk.CTkFont(size=12), command=self._select_all,
                      ).pack(side="left", padx=(0, 8))
        ctk.CTkButton(top_bar, text="Deseleccionar todo", width=140, height=28,
                      fg_color="#2a2a4a", hover_color="#3a3a6a", text_color="#ccccff",
                      font=ctk.CTkFont(size=12), command=self._deselect_all,
                      ).pack(side="left")

        # Scrollable list
        scroll = ctk.CTkScrollableFrame(self, fg_color="transparent")
        scroll.pack(fill="both", expand=True, padx=22, pady=(0, 16))

        for opt in self._opts:
            self._add_card(scroll, opt)

    def _add_card(self, parent, opt: dict):
        bg, badge_color, risk_label = RISK_MAP.get(opt["risk"], RISK_MAP["low"])

        card = ctk.CTkFrame(parent, fg_color=BG_CARD, corner_radius=12)
        card.pack(fill="x", pady=5, padx=4)

        inner = ctk.CTkFrame(card, fg_color="transparent")
        inner.pack(fill="x", padx=16, pady=12)
        inner.columnconfigure(1, weight=1)

        var = ctk.BooleanVar(value=opt.get("default", False))
        self._vars[opt["id"]] = var

        sw = ctk.CTkSwitch(
            inner, text="", variable=var, width=46,
            button_color=ACCENT, button_hover_color="#c62333",
            progress_color="#3a0a10", fg_color="#333355",
            onvalue=True, offvalue=False,
        )
        sw.grid(row=0, column=0, rowspan=2, sticky="ns", padx=(0, 14))
        self._switches[opt["id"]] = sw

        name_row = ctk.CTkFrame(inner, fg_color="transparent")
        name_row.grid(row=0, column=1, sticky="ew")
        name_row.columnconfigure(0, weight=1)

        ctk.CTkLabel(name_row, text=opt["name"],
                     font=ctk.CTkFont(size=13, weight="bold"), text_color="#e8e8ff",
                     anchor="w",
                     ).grid(row=0, column=0, sticky="w")

        badge_frame = ctk.CTkFrame(name_row, fg_color=bg, corner_radius=6, width=60, height=20)
        badge_frame.grid(row=0, column=1, padx=(10, 0))
        badge_frame.grid_propagate(False)
        ctk.CTkLabel(badge_frame, text=f"  {risk_label}  ",
                     font=ctk.CTkFont(size=10, weight="bold"), text_color=badge_color,
                     ).place(relx=0.5, rely=0.5, anchor="center")

        ctk.CTkLabel(inner, text=opt["description"],
                     font=ctk.CTkFont(size=11), text_color=TEXT_DIM,
                     anchor="w", justify="left", wraplength=680,
                     ).grid(row=1, column=1, sticky="w", pady=(4, 0))

    def _select_all(self):
        for var in self._vars.values():
            var.set(True)

    def _deselect_all(self):
        for var in self._vars.values():
            var.set(False)

    def get_selected_opts(self) -> list[dict]:
        return [opt for opt in self._opts if self._vars.get(opt["id"], ctk.BooleanVar()).get()]
