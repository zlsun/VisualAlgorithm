
from PyQt4.QtCore import *
from PyQt4.QtGui import *

class Base(object):

    def __init__(self):
        self.mark_color = {}
        self.mark_value = {}

    def draw(self, visualization, painter):
        pass

    def add_mark(self, name, color):
        self.mark_color[name] = color
        self.mark_value[name] = None

    def update_mark(self, f_globals, f_locals):
        for name in self.mark_value.keys():
            if name in f_locals:
                self.mark_value[name] = f_locals[name]
                continue
            if name in f_globals:
                self.mark_value[name] = f_globals[name]
                continue
            self.mark_value[name] = None

    def remove_mark(self, name):
        del self.mark_color[name]
        del self.mark_value[name]

    def get_pen_color(self, value):
        return None

    def get_brush_color(self, value):
        for name in self.mark_color.keys():
            if self.mark_value[name] == value:
                return QColor(self.mark_color[name])
        return None
