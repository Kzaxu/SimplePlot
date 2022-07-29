from ..serializable.jsonable import Jsonable


class PlotConfig(Jsonable):

    def to_params(self):
        return self.to_json()
