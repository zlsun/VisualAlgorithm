
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Base(object):

    def __init__(self):
        self.bind_vars = {}
        self.bind_colors = {}

    def draw(self, visualization, painter):
        pass

    def bind(self, name, color):
        self.bind_vars[name] = None
        self.bind_colors[name] = color

    def update_bind(self, f_globals, f_locals):
        for name in self.bind_vars.keys():
            if name in f_locals:
                self.bind_vars[name] = f_locals[name]
                continue
            if name in f_globals:
                self.bind_vars[name] = f_globals[name]
                continue
            self.bind_vars[name] = None

    def unbind(self, name):
        del self.bind_vars[name]
        del self.bind_colors[name]

    def get_pen(self, value):
        return None

    def get_brush(self, value):
        for name in self.bind_vars.keys():
            if self.bind_vars[name] == value:
                return QColor(self.bind_colors[name])
        return None
