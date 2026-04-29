from app.ui.pages.base_page import OptimizationPage
from app.optimizations.definitions import OPTIMIZATIONS


class NetworkPage(OptimizationPage):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title="Red",
            description="Reduce ping y latencia: TCP, DNS, QoS y throttling de red.",
            optimizations=OPTIMIZATIONS["network"],
            get_selected_callback=lambda: self.get_selected_opts(),
            **kwargs,
        )
