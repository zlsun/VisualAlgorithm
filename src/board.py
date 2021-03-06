
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from visualization import Visualization


class Board(QMdiArea):

    def __init__(self, parent=None):
        QMdiArea.__init__(self, parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def addVar(self, name):
        widget = Visualization(name)
        widget.setWindowTitle(name)
        self.addSubWindow(widget)
        widget.show()

    def getVars(self):
        return (w.widget() for w in self.subWindowList())

