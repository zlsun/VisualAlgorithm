
from .base import *
from .list import List


class Matrix(Base):

    def __init__(self, value=[[]]):
        Base.__init__(self)
        self.value = value
        self.color_map = {1: 0x000000, 0: 0xffffff}

    def __getitem__(self, i):
        if type(i) == int:
            return List(self.value[i])
        elif type(i) == tuple:
            r, c = i
            return self.value[r][c]

    def __setitem__(self, i, value):
        if type(i) == int:
            self.value[i] = value
        elif type(i) == tuple:
            r, c = i
            self.value[r][c] = value

    def add_color(self, data, color):
        self.color_map[data] = color

    def get_pen_color(self, index):
        return Base.get_pen_color(self, index) or QColor(0x000000)

    def get_brush_color(self, pos):
        color = Base.get_brush_color(self, pos)
        if color:
            return color
        data = self[pos]
        if self.color_map.has_key(data):
            return QColor(self.color_map[data])
        return QColor(0x808080)

    def draw(self, visualization, painter):
        w, h = visualization.width(), visualization.height()
        rows = len(self.value)
        cols = len(self.value[0])
        if rows == 0 or cols == 0:
            return
        tile_size = min(w / cols, h / rows)

        painter.translate(
            (w - tile_size * cols) / 2, (h - tile_size * rows) / 2)
        painter.scale(1, 1)
        y = 0
        for i in range(rows):
            x = 0
            for j in range(cols):
                painter.setPen(self.get_pen_color((i, j)))
                painter.setBrush(self.get_brush_color((i, j)))
                painter.drawRect(x, y, tile_size, tile_size)
                x += tile_size
            y += tile_size
