from app.ui.pages.base_page import OptimizationPage
from app.optimizations.definitions import OPTIMIZATIONS


class AdvancedPage(OptimizationPage):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title="Avanzado",
            description="⚠ Tweaks de mayor riesgo. Lee cada descripción antes de activarlos. Algunos requieren reiniciar para aplicarse completamente.",
            optimizations=OPTIMIZATIONS["advanced"],
            get_selected_callback=lambda: self.get_selected_opts(),
            **kwargs,
        )
