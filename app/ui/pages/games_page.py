from app.ui.pages.base_page import OptimizationPage
from app.optimizations.definitions import OPTIMIZATIONS


class GamesPage(OptimizationPage):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title="Juegos",
            description="Perfiles de prioridad por juego (Fortnite, Valorant, CS2) y Game Mode de Windows.",
            optimizations=OPTIMIZATIONS["games"],
            get_selected_callback=lambda: self.get_selected_opts(),
            **kwargs,
        )
