from app.ui.pages.base_page import OptimizationPage
from app.optimizations.definitions import OPTIMIZATIONS


class SystemPage(OptimizationPage):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title="Sistema",
            description="Optimizaciones del sistema operativo: energía, servicios, planificador de CPU y efectos visuales.",
            optimizations=OPTIMIZATIONS["system"],
            get_selected_callback=lambda: self.get_selected_opts(),
            **kwargs,
        )
