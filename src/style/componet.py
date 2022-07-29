from .plot_config import PlotConfig


class Limit(PlotConfig):
    """
    控制 x,y 轴上下界
    """
    lower:float
    upper:float

    def __init__(self, lower, upper) -> None:
        self.lower = lower
        self.upper = upper

    def to_params(self):
        return [self.lower, self.upper]