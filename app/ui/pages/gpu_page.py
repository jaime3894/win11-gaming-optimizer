from app.ui.pages.base_page import OptimizationPage
from app.optimizations.definitions import OPTIMIZATIONS


class GpuPage(OptimizationPage):
    def __init__(self, parent, **kwargs):
        super().__init__(
            parent,
            title="GPU",
            description="Tweaks de GPU para reducir input lag y mejorar frame pacing. Las opciones [NVIDIA]/[AMD] solo aplican a su vendor.",
            optimizations=OPTIMIZATIONS["gpu"],
            get_selected_callback=lambda: self.get_selected_opts(),
            **kwargs,
        )
