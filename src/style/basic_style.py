from .componet import Limit
from .plot_config import PlotConfig

class BasicStyle(PlotConfig):
    title:str

    # x,y 轴标签
    xlabel:str
    ylabel:str

    xlim:Limit
    ylim:Limit
    pass


