#-*- encoding: utf-8 -*-

import sys
from bdb import Bdb
from time import time, sleep

from PyQt4.QtCore import *


class Sdb(Bdb):

    def __init__(self):
        Bdb.__init__(self)
        self.line_handler = None
        self.globals = {}
        self.locals = self.globals

    def run(self, script):
        Bdb.run(self, script, self.globals, self.locals)

    def set_line_handler(self, handler):
        self.line_handler = handler

    def user_line(self, frame):
        # self.curframe = frame
        if frame.f_code.co_filename != '<string>':
            return
        # if frame.f_lineno != self.last_lineno:
        if self.line_handler:
            self.line_handler(frame)
        self.last_lineno = frame.f_lineno


class Debugger(QThread):

    def __init__(self, script, timeout=500, step_mode=False):
        QThread.__init__(self)
        self.sdb = Sdb()
        self.script = script
        self.sdb.set_line_handler(self.line_handler)
        self.step_mode = step_mode
        self.active = False
        self.running = False
        self.setTimeout(timeout)
        self.onQuit.connect(self.sdb.set_quit)

    onLineCallback  = pyqtSignal(object)
    onException     = pyqtSignal(object)
    onQuit          = pyqtSignal()

    def line_handler(self, frame):
        # print "line_handler in", int(QThread.currentThreadId()), 'on', time()
        self.onLineCallback.emit(frame)
        if self.step_mode:
            self.active = False
        if self.active:
            sleep(self.timeout)
        while not self.active:
            sleep(0.01)

    def setTimeout(self, timeout):
        self.timeout = timeout / 1000.0

    def run(self):
        # print "run in", int(QThread.currentThreadId()), 'on', time()
        self.active = True
        self.running = True
        try:
            self.sdb.run(self.script)
        except:
            self.onException.emit(sys.exc_info())
        if self.running:
            self.stop()

    def pause(self):
        print "pause in", int(QThread.currentThreadId()), 'on', time()
        self.active = False

    def resume(self, step_mode=False):
        print "resume in", int(QThread.currentThreadId()), 'on', time()
        self.step_mode = step_mode
        self.active = True

    def stop(self):
        print "stop in", int(QThread.currentThreadId()), 'on', time()
        self.running = False
        self.onQuit.emit()
