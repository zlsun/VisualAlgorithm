
from PyQt4.QtCore import *
from PyQt4.QtGui import *

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
        self.value.draw(self, painter)

    def updateValue(self, value, f_globals, f_locals):
        self.value = value
        self.value.update_mark(f_globals, f_locals)
        self.update()
