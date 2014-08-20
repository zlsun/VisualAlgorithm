
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from visualization import Visualization


class Board(QMdiArea):

    def __init__(self, parent=None):
        QMdiArea.__init__(self, parent)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

    def addVisualization(self, name):
        widget = Visualization(name)
        widget.setWindowTitle(name)
        self.addSubWindow(widget)
        widget.show()

    def getVisualizations(self):
        return (w.widget() for w in self.subWindowList())
