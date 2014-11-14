
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.Qsci import (
    QsciScintilla,
    QsciLexerPython
)


class Editor(QsciScintilla):

    def __init__(self, parent=None):
        QsciScintilla.__init__(self, parent)

        self.setUtf8(True)
        self.setFont(QFont('Consolas', 10))
        self.setLexer(QsciLexerPython())

        self.setMarginLineNumbers(1, True)

        self.setTabWidth(4)
        self.setAutoIndent(True)
        self.setIndentationGuides(True)
        self.setIndentationsUseTabs(False)
        self.setBackspaceUnindents(True)

        self.setWrapMode(QsciScintilla.WrapWord)
        self.setWrapIndentMode(QsciScintilla.WrapIndentIndented)

        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        self.setFolding(QsciScintilla.PlainFoldStyle)

        self.context_menu = None
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.onContextMenuRequested)

        self.linesChanged.connect(
            lambda: self.setMarginWidth(1, ' %d' % self.lines())
        )

    def highlightLine(self, lineno):
        self.setSelection(
            lineno,
            0,
            lineno,
            len(self.text(lineno).replace('\r', '').replace('\n', ''))
        )

    def clearSelection(self):
        self.setSelection(0,  0,  0,  0)

    def setContextMenu(self, menu):
        self.context_menu = menu

    def onContextMenuRequested(self, coord):
        if self.context_menu:
            self.context_menu.popup(self.mapToGlobal(coord))
