
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from structures import *


class Visualization(QWidget):

    def __init__(self, name, parent=None):
        QWidget.__init__(self, parent)
        self.setMinimumSize(400, 200)
        self.name = name
        self.value = Base()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        draw = getattr(self.value, "draw", None)
        if callable(draw):
            draw(self, painter)

    def updateValue(self, value, f_globals, f_locals):
        self.value = value
        self.value.update_bind(f_globals, f_locals)
        self.update()

