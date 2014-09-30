
from .base import *


class List(Base, list):

    def __init__(self, value=[]):
        Base.__init__(self)
        list.__init__(self, value)

    def get_pen(self, index):
        return Base.get_pen(self, index) or QColor(0x000000)

    def get_brush(self, index):
        return Base.get_brush(self, index) or QColor(0x0080FF)

    def draw(self, visualization, painter):
        w, h = visualization.width(), visualization.height()
        length = len(self)
        if length == 0:
            return
        wi = float(w) / length
        mh = max(self)
        x = 0
        painter.translate(0, h)
        painter.scale(1, 1)
        for i in range(length):
            painter.setPen(self.get_pen(i))
            painter.setBrush(self.get_brush(i))
            height = self[i] * h / mh
            painter.drawRect(x, - height, wi, height)
            x += wi
