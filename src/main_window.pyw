#!/usr/bin/env python3
#-*- encoding: utf-8 -*-

import os
from time import time

from PyQt5.QtCore import *
from PyQt5.QtGui  import *
from PyQt5.QtWidgets import *

from debugger import Debugger
from editor import Editor
from board import Board
from structures import Base

DEBUG = True

ENCODING = 'utf-8'

APP_NAME      = 'VisualAlgorithm'
UNTITLED      = 'Untitled.py'
ICONS_DIR     = './icons/'
APP_ICON_PATH = os.path.join(ICONS_DIR, 'icon.ico')


def strippedName(filePath):
    return QFileInfo(filePath).fileName() if filePath else UNTITLED


class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.debugger = None
        self.setupUi()

        if DEBUG:
            for f, v in [
                ('sort', 'L'),
                ('maze', 'maze'),
                ('binary_tree', 'tree'),
                ('rb_tree', 'tree')
            ]:
                filePath = './examples/{}.py'.format(f)
                tab = self.addTab(strippedName(filePath))
                tab.filePath = filePath
                with open(filePath, 'r', encoding=ENCODING) as f:
                    data = f.read()
                    tab.editor.setText(data)
                    tab.editor.setModified(False)
                    tab.board.addVar(v)

    def setupUi(self):
        self.resize(800, 600)
        self.setWindowTitle(APP_NAME)

        self.createActions()
        self.createMenus()
        self.createToolBars()
        self.createSlider()
        self.createStatusBar()
        self.createContextMenu()

        self.centralWidget = QWidget()
        layout = QHBoxLayout(self.centralWidget)
        layout.setContentsMargins(5, 5, 5, 5)

        self.tabWidget = QTabWidget()
        self.tabWidget.setMovable(True)
        self.tabWidget.setTabsClosable(True)
        self.tabWidget.tabCloseRequested.connect(self.closeFile)
        self.tabWidget.currentChanged.connect(lambda index: self.stop())

        layout.addWidget(self.tabWidget)
        self.setCentralWidget(self.centralWidget)

    def addTab(self, title):
        tab = QWidget()
        tab.filePath = None

        layout = QHBoxLayout(tab)
        layout.setContentsMargins(5, 5, 5, 5)

        splitter = QSplitter()
        splitter.setOrientation(Qt.Horizontal)

        tab.editor = Editor(splitter)
        tab.editor.setContextMenu(self.context_menu)
        tab.editor.cursorPositionChanged.connect(
            lambda line, index:
                self.indicatorLabel.setText(
                    '第 {} 行, 第 {} 列'.format(line + 1, index + 1)
                )
        )
        tab.editor.modificationChanged.connect(
            lambda m:
                self.tabWidget.setTabText(
                    self.tabWidget.indexOf(tab),
                    title + ' *' * m
                )
        )

        tab.board = Board(splitter)

        layout.addWidget(splitter)

        self.tabWidget.addTab(tab, title)
        self.tabWidget.setCurrentWidget(tab)

        return tab

    def addActionsTo(self, target, actions):
        for act in actions.split():
            if act == '|':
                target.addSeparator()
            else:
                target.addAction(self.actions[act])

    def createActions(self):
        def A(text, slot, shortcut=None, icon=None):
            action = QAction(text, self)
            action.triggered.connect(lambda checked: slot())
            if shortcut:
                action.setShortcut(shortcut)
                action.setToolTip(
                    '{} ({})'.format(
                        text[:text.find('(')].replace('...', ''),
                        action.shortcut().toString()
                    )
                )
            if icon:
                action.setIcon(QIcon(os.path.join(ICONS_DIR, icon)))
            return action

        self.actions = {
            'New'       : A('新建(&N)',      self.newFile,   QKeySequence.New,             'new.png'       ),
            'Open'      : A('打开...(&O)',   self.openFiles, QKeySequence.Open,            'open.png'      ),
            'Close'     : A('关闭(&C)',      self.closeFile, QKeySequence.Close,           'close.png'     ),
            'CloseAll'  : A('关闭全部(&E)',  self.closeAll,  QKeySequence('ctrl+shift+w'), 'closeAll.png'  ),
            'Save'      : A('保存(&S)',      self.saveFile,  QKeySequence.Save,            'fileSave.png'  ),
            'SaveAll'   : A('另存为...(&A)', self.saveAs,    QKeySequence('ctrl+shift+s'), 'fileSaveAs.png'),
            'Quit'      : A('退出(&Q)',      self.close,     QKeySequence('ctrl+q')                        ),
            'Undo'      : A('撤销(&U)',      self.undo,      QKeySequence.Undo,            'editUndo.png'  ),
            'Redo'      : A('重做(&R)',      self.redo,      QKeySequence.Redo,            'editRedo.png'  ),
            'Cut'       : A('剪切(&X)',      self.cut,       QKeySequence.Cut,             'editCut.png'   ),
            'Copy'      : A('复制(&C)',      self.copy,      QKeySequence.Copy,            'editCopy.png'  ),
            'Paste'     : A('粘贴(&P)',      self.paste,     QKeySequence.Paste,           'editPaste.png' ),
            'SeleteAll' : A('全选(&A)',      self.selectAll, QKeySequence.SelectAll                        ),
            'Run'       : A('运行(&R)',      self.run,       QKeySequence('F5'),           'run.png'       ),
            'Step'      : A('单步(&P)',      self.step,      QKeySequence('F6'),           'step.png'      ),
            'Resume'    : A('暂停(&E)',      self.pause,     QKeySequence('F7'),           'pause.png'     ),
            'Stop'      : A('停止(&S)',      self.stop,      QKeySequence('F8'),           'stop.png'      ),
            'AddVis'    : A('添加变量(&A)',  self.addVar,    QKeySequence('F9')                            ),
            'Help'      : A('帮助(&H)',      self.help,      QKeySequence('F1')                            ),
            'About'     : A('关于(&A)',      self.about                                                    ),
        }

    def createMenus(self):
        menus = [
            ('文件(&F)', 'New  Open | Close CloseAll | Save SaveAll | Quit'),
            ('编辑(&E)', 'Undo Redo | Cut Copy Paste | SeleteAll'),
            ('开始(&S)', 'Run Step Resume Stop | AddVis'),
            ('帮助(&H)', 'Help About')
        ]
        for m in menus:
            self.addActionsTo(self.menuBar().addMenu(m[0]), m[1])

    def createToolBars(self):
        bars = [
            ('文件', 'New  Open | Close CloseAll | Save SaveAll'),
            ('编辑', 'Undo Redo | Cut Copy Paste'),
            ('开始', 'Run Step Resume Stop'),
        ]
        for m in bars:
            self.addActionsTo(self.addToolBar(m[0]), m[1])

    def createContextMenu(self):
        self.context_menu = QMenu('Context Menu')
        self.addActionsTo(self.context_menu, 'Undo Redo | Cut Copy Paste | SeleteAll | AddVis')

    def createSlider(self):
        toolbar = self.addToolBar('slider')
        self.slider = QSlider(Qt.Horizontal)
        self.sliderLabel = QLabel()
        toolbar.addWidget(self.slider)
        toolbar.addWidget(self.sliderLabel)

        self.slider.valueChanged.connect(self.setTimeout)
        self.slider.setValue(50)

    def createStatusBar(self):
        statusBar = self.statusBar()
        self.indicatorLabel = QLabel()
        statusBar.addPermanentWidget(self.indicatorLabel)

    def currentTab(self):
        return self.tabWidget.currentWidget()

    def checkTab(method):
        def decorated(main_window, *args, **kwds):
            tab = main_window.currentTab()
            if not tab:
                return False
            method.__globals__['tab'] = tab
            return method(main_window, *args, **kwds)
        return decorated

    @checkTab
    def maybeSave(self):
        if tab.editor.isModified():
            msgBox = QMessageBox()
            msgBox.setText('文件 {} 已被修改'.format(strippedName(tab.filePath)))
            msgBox.setInformativeText('你想保存吗?')
            btnSave    = msgBox.addButton('保存(&S)', QMessageBox.YesRole)
            btnDiscard = msgBox.addButton('丢弃(&D)', QMessageBox.NoRole)
            btnCancel  = msgBox.addButton('取消(&C)', QMessageBox.RejectRole)
            msgBox.setDefaultButton(btnSave)
            msgBox.exec_()
            if msgBox.clickedButton() == btnSave:
                return self.saveFile()
            elif msgBox.clickedButton() == btnCancel:
                return False
        return True

    def setTimeout(self, timeout):
        self.sliderLabel.setText('{}ms'.format(timeout))
        if self.debugger:
            self.debugger.setTimeout(timeout)

    def newFile(self):
        self.addTab(UNTITLED)

    def openFiles(self):
        filePaths, _ = QFileDialog.getOpenFileNames(
            self,
            caption='打开文件',
            filter='Python文件 (*.py *.pyw);;所有文件 (*.*)'
        )
        if not filePaths:
            return
        for filePath in filePaths:
            tab = self.addTab(strippedName(filePath))
            tab.filePath = filePath
            with open(filePath, 'r', encoding=ENCODING) as f:
                data = f.read()
                tab.editor.setText(data)
                tab.editor.setModified(False)

    @checkTab
    def closeFile(self, index=None):
        if self.maybeSave():
            index = index or self.tabWidget.currentIndex()
            self.tabWidget.removeTab(index)
            return True
        return False

    def closeAll(self):
        while self.tabWidget.count():
            if not self.closeFile():
                return False
        return True

    def saveTab(self, tab):
        try:
            with open(tab.filePath, 'w', encoding=ENCODING) as f:
                f.write(tab.editor.text())
            tab.editor.setModified(False)
            self.statusBar().showMessage('文件已保存', 2000)
            return True
        except:
            self.statusBar().showMessage('无法保存文件', 2000)
            return False

    @checkTab
    def saveFile(self):
        return self.saveTab(tab) if tab.filePath else self.saveAs()

    @checkTab
    def saveAs(self):
        filePath = QFileDialog.getSaveFileName(
            self,
            caption='另存为',
            filter='Python文件 (*.py *.pyw);;所有文件 (*.*)'
        )
        if not filePath:
            return False
        tab.filePath = filePath
        self.tabWidget.setTabText(
            self.tabWidget.currentIndex(), strippedName(tab.filePath))
        return self.saveTab(tab)

    for a in 'undo redo cut copy paste selectAll'.split():
        locals()[a] = checkTab(
            lambda self, a=a: tab.editor.__getattribute__(a)()
        )

    @checkTab
    def onLineCallback(self, frame):
        # print('onLineCallback in', int(QThread.currentThreadId()), 'on', time())
        tab.editor.highlightLine(frame.f_lineno - 1)
        for v in tab.board.getVars():
            f_globals = frame.f_globals
            f_locals = frame.f_locals
            name = v.name
            if name in f_locals:
                value = f_locals[name]
            elif name in f_globals:
                value = f_globals[name]
            else:
                value = Base()
            v.updateValue(value, f_globals, f_locals)

    @checkTab
    def onQuit(self):
        tab.editor.clearSelection()

    def onException(self, exc_info):
        import traceback
        import io

        with io.StringIO() as output:
            exc_type, exc_value, exc_traceback = exc_info
            exc_traceback = exc_traceback.tb_next.tb_next
            traceback.print_exception(
                exc_type,
                exc_value,
                exc_traceback,
                limit=10,
                file=output
            )
            msgBox = QMessageBox()
            msgBox.setWindowTitle('Error')
            msgBox.setText(output.getvalue())
            msgBox.setButtonText(QMessageBox.Ok, '关闭(&C)')
            msgBox.exec_()

    @checkTab
    def run(self, step_mode=False):
        # print('run in', int(QThread.currentThreadId()), 'on', time())
        if not self.debugger or not self.debugger.running:
            script = tab.editor.text()
            self.debugger = Debugger(
                script,
                timeout=self.slider.value(),
                step_mode=step_mode
            )
            self.debugger.onLineCallback.connect(self.onLineCallback)
            self.debugger.onQuit.connect(self.onQuit)
            self.debugger.onException.connect(self.onException)
            self.debugger.start()
        elif self.debugger.running and not self.debugger.active:
            self.debugger.resume(step_mode)

    def step(self):
        self.run(step_mode=True)

    def pause(self):
        if self.debugger and self.debugger.running and self.debugger.active:
            self.debugger.pause()

    def stop(self):
        if self.debugger and self.debugger.running:
            self.debugger.stop()

    @checkTab
    def addVar(self):
        tab.board.addVar(tab.editor.selectedText())

    def help(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle("帮助")
        msgBox.setText('''
        <h1> 使用方法 </h1>
        <ol>
            <li> 点击“文件”—“打开”，打开要运行的算法文件，本软件自带示例在 examples 文件夹下。 </li>
            <li> 在左侧的编辑器中，选中要可视化的数据结构变量名，右键—“添加变量”。</li>
            <li> 点击工具栏上的“运行”按钮，开始执行算法。在算法运行过程中，
                 可以通过工具栏进行暂停、单步运行、停止以及调整运行速度等操作。
            </li>
        </ol>
        ''')
        msgBox.addButton('关闭(&C)', QMessageBox.AcceptRole)
        msgBox.exec_()

    def about(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(APP_NAME)
        msgBox.setIconPixmap(QPixmap(APP_ICON_PATH))
        msgBox.setText('''
            <br/>
            <h1 align='center'> VisualAlgorithm </h1>
            <p align='right'>
                <h2> v1.0.0 </h2>
            </p>
            <br/>
            <p align='center'> Copyright (c) zlsun </p>
        ''')
        msgBox.addButton('关闭(&C)', QMessageBox.AcceptRole)
        msgBox.exec_()

    def closeEvent(self, event):
        if self.closeAll():
            if self.debugger:
                self.stop()
            return event.accept()
        else:
            return event.ignore()


if __name__ == '__main__':
    import sys

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(APP_ICON_PATH))
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())

