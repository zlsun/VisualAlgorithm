#-*- encoding: utf-8 -*-

from os import chdir, listdir
from os.path import split
from time import time

from PyQt4.QtCore import *
from PyQt4.QtGui import *

from debugger import Debugger
from editor import Editor
from board import Board
from structures import Base

DEBUG = True

APP_NAME      = u'VisualAlgorithm'
UNTITLED      = u'Untitled.py'
ICONS_PATH    = u'./icons/'
APP_ICON_PATH = ICONS_PATH + u'icon.png'


def qstring2str(qstr):
    return unicode(qstr, 'u8', 'ignore').encode('u8')

def strippedName(filePath):
    return QFileInfo(filePath).fileName() if filePath else UNTITLED

def addActionsTo(target, actions):
    for action in actions:
        if not action:
            target.addSeparator()
        else:
            target.addAction(action)

class MainWindow(QMainWindow):

    def __init__(self, parent=None):
        QMainWindow.__init__(self, parent)
        self.debugger = None
        self.setupUi()

        if DEBUG:
            for f, v in [('sort', 'L'), ('maze', 'maze'), ('binary_tree', 'tree'), ('rb_tree', 'tree')]:
                filePath = './examples/%s.py' % f
                tab = self.addTab(strippedName(filePath))
                tab.filePath = filePath
                with open(qstring2str(filePath), 'rb') as f:
                    data = f.read()
                    tab.editor.setText(data)
                    tab.editor.setModified(False)
                    tab.board.addVisualization(v)

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
            lambda line, index: self.indicatorLabel.setText(u'第 %d 行, 第 %d 列' % (line + 1, index + 1)))
        tab.editor.modificationChanged.connect(
            lambda m: self.tabWidget.setTabText(self.tabWidget.indexOf(tab), title + ' *' * m))

        tab.board = Board(splitter)

        layout.addWidget(splitter)

        self.tabWidget.addTab(tab, title)
        self.tabWidget.setCurrentWidget(tab)

        return tab

    def createActions(self):
        def A(text, slot, shortcut=None, icon=None):
            action = QAction(text, self)
            self.connect(action, SIGNAL('triggered()'), slot)
            if shortcut:
                action.setShortcut(shortcut)
                action.setToolTip("%s (%s)" %
                                 (text[:text.find('(')].replace('...', ''), action.shortcut().toString()))
            if icon:
                action.setIcon(QIcon(ICONS_PATH + icon))
            return action

        actions = {
            'New':       A(u'新建(&N)',      self.newFile,   QKeySequence.New,             'new.png'       ),
            'Open':      A(u'打开...(&O)',   self.openFiles, QKeySequence.Open,            'open.png'      ),
            'Close':     A(u'关闭(&C)',      self.closeFile, QKeySequence('ctrl+w'),       'close.png'     ),
            'CloseAll':  A(u'关闭全部(&E)',  self.closeAll,  QKeySequence('ctrl+shift+w'), 'closeAll.png'  ),
            'Save':      A(u'保存(&S)',      self.saveFile,  QKeySequence.Save,            'fileSave.png'  ),
            'SaveAll':   A(u'另存为...(&A)', self.saveAs,    QKeySequence('ctrl+shift+s'), 'fileSaveAs.png'),
            'Quit':      A(u'退出(&Q)',      self.close,     QKeySequence('ctrl+q')                        ),
            'Undo':      A(u'撤销(&U)',      self.undo,      QKeySequence.Undo,            'editUndo.png'  ),
            'Redo':      A(u'重做(&R)',      self.redo,      QKeySequence.Redo,            'editRedo.png'  ),
            'Cut':       A(u'剪切(&X)',      self.cut,       QKeySequence.Cut,             'editCut.png'   ),
            'Copy':      A(u'复制(&C)',      self.copy,      QKeySequence.Copy,            'editCopy.png'  ),
            'Paste':     A(u'粘贴(&P)',      self.paste,     QKeySequence.Paste,           'editPaste.png' ),
            'SeleteAll': A(u'全选(&A)',      self.selectAll, QKeySequence.SelectAll                        ),
            'Run':       A(u'运行(&R)',      self.run,       QKeySequence('F5'),           'run.png'       ),
            'Step':      A(u'单步(&P)',      self.step,      QKeySequence('F11'),          'step.png'      ),
            'Resume':    A(u'暂停(&E)',      self.pause,     QKeySequence('F6'),           'pause.png'     ),
            'Stop':      A(u'停止(&S)',      self.stop,      QKeySequence('F12'),          'stop.png'      ),
            'About':     A(u'关于(&A)',      self.about                                                    ),
            'AddVisualization':
                A(u'添加可视化变量(&A)', self.addVisualization, QKeySequence('F2')),
        }
        self.__dict__.update({'action%s' % k: v for k, v in actions.items()})

    def createMenus(self):
        map(lambda m: addActionsTo(self.menuBar().addMenu(m[0]), m[1]), [
            (u'文件(&F)', [
                self.actionNew,     self.actionOpen,        None,
                self.actionClose,   self.actionCloseAll,    None,
                self.actionSave,    self.actionSaveAll,     None,
                self.actionQuit
            ]),
            (u'编辑(&E)', [
                self.actionUndo,    self.actionRedo,        None,
                self.actionCut,     self.actionCopy,        self.actionPaste,   None,
                self.actionSeleteAll
            ]),
            (u'开始(&S)', [
                self.actionRun,     self.actionStep,        self.actionResume,  self.actionStop,    None,
                self.actionAddVisualization
            ]),
            (u'帮助(&H)', [
                self.actionAbout
            ])
        ])

    def createToolBars(self):
        map(lambda m: addActionsTo(self.addToolBar(m[0]), m[1]), [
            (u'文件', [
                self.actionNew,     self.actionOpen,        None,
                self.actionClose,   self.actionCloseAll,    None,
                self.actionSave,    self.actionSaveAll,
            ]),
            (u'编辑', [
                self.actionUndo,    self.actionRedo,        None,
                self.actionCut,     self.actionCopy,        self.actionPaste,
            ]),
            (u'开始', [
                self.actionRun,     self.actionStep,        self.actionResume,  self.actionStop,
            ]),
        ])

    def createContextMenu(self):
        self.context_menu = QMenu(u'Context Menu')
        addActionsTo(self.context_menu, [
            self.actionUndo,        self.actionRedo,    None,
            self.actionCut,         self.actionCopy,    self.actionPaste,   None,
            self.actionSeleteAll,   None,
            self.actionAddVisualization
        ])

    def createSlider(self):
        toolbar = self.addToolBar(u'滑动条')
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
        def decorated(*args, **kwds):
            tab = args[0].currentTab()
            if not tab:
                return False
            method.func_globals['tab'] = tab
            return method(*args, **kwds)
        return decorated

    @checkTab
    def maybeSave(self):
        if tab.editor.isModified():
            msgBox = QMessageBox()
            msgBox.setText(u'文件 %s 已被修改' % strippedName(tab.filePath))
            msgBox.setInformativeText(u'你想保存吗?')
            btnSave    = msgBox.addButton(u'保存(&S)', QMessageBox.YesRole)
            btnDiscard = msgBox.addButton(u'丢弃(&D)', QMessageBox.NoRole)
            btnCancel  = msgBox.addButton(u'取消(&C)', QMessageBox.RejectRole)
            msgBox.setDefaultButton(btnSave)
            msgBox.exec_()
            if msgBox.clickedButton() == btnSave:
                return self.saveFile()
            elif msgBox.clickedButton() == btnCancel:
                return False
        return True

    def setTimeout(self, timeout):
        self.sliderLabel.setText(u'%dms' % timeout)
        if self.debugger:
            self.debugger.setTimeout(timeout)

    def newFile(self):
        self.addTab(UNTITLED)

    def openFiles(self):
        filePaths = QFileDialog.getOpenFileNames(self, caption=u'打开文件',
                                                 filter=u'Python文件 (*.py *.pyw);;所有文件 (*.*)')
        if not filePaths:
            return
        for filePath in filePaths:
            tab = self.addTab(strippedName(filePath))
            tab.filePath = filePath
            with open(qstring2str(filePath), 'rb') as f:
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
            with open(qstring2str(tab.filePath), 'wb') as f:
                f.write(qstring2str(tab.editor.text()))
            tab.editor.setModified(False)
            self.statusBar().showMessage(u'文件已保存', 2000)
            return True
        except:
            self.statusBar().showMessage(u'无法保存文件', 2000)
            return False

    @checkTab
    def saveFile(self):
        return self.saveTab(tab) if tab.filePath else self.saveAs()

    @checkTab
    def saveAs(self):
        filePath = QFileDialog.getSaveFileName(self, caption=u'另存为',
                                               filter=u'Python文件 (*.py *.pyw);;所有文件 (*.*)')
        if not filePath:
            return False
        tab.filePath = filePath
        self.tabWidget.setTabText(self.tabWidget.currentIndex(), strippedName(tab.filePath))
        return self.saveTab(tab)

    for f in ['undo', 'redo', 'cut', 'copy', 'paste', 'selectAll']:
        locals()[f] = checkTab(lambda self, f=f: tab.editor.__getattribute__(f)())

    @checkTab
    def onLineCallback(self, frame):
        # print "onLineCallback in", int(QThread.currentThreadId()), 'on', time()
        tab.editor.highlightLine(frame.f_lineno - 1)
        for v in tab.board.getVisualizations():
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

        with io.BytesIO() as output:
            exc_type, exc_value, exc_traceback = exc_info
            exc_traceback = exc_traceback.tb_next.tb_next
            traceback.print_exception(exc_type, exc_value, exc_traceback, limit=10, file=output)
            msgBox = QMessageBox()
            msgBox.setWindowTitle(u'Error')
            msgBox.setText(output.getvalue() )
            msgBox.setButtonText(QMessageBox.Ok, u'关闭(&C)')
            msgBox.exec_()

    @checkTab
    def run(self, step_mode=False):
        print "run in", int(QThread.currentThreadId()), 'on', time()
        if not self.debugger or not self.debugger.running:
            script = qstring2str(tab.editor.text())
            self.debugger = Debugger(script, timeout=self.slider.value(), step_mode=step_mode)
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
    def addVisualization(self):
        tab.board.addVisualization(tab.editor.selectedText())

    def about(self):
        msgBox = QMessageBox()
        msgBox.setWindowTitle(APP_NAME)
        msgBox.setIconPixmap(QPixmap(APP_ICON_PATH))
        msgBox.setText(u'''
            <br/>
            <h1 align='center'> VisualAlgorithm </h1>
            <p align='right'>
                <h2> v1.0.0 </h2>
            </p>
            <br/>
            <p align='center'> Made by zl@sun </p>
        ''')
        msgBox.setButtonText(QMessageBox.Ok, u'关闭(&C)')
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

    mycode = 'UTF-8'
    code = QTextCodec.codecForName(mycode)
    QTextCodec.setCodecForCStrings(code)

    app = QApplication(sys.argv)
    app.setWindowIcon(QIcon(APP_ICON_PATH))
    wnd = MainWindow()
    wnd.show()
    sys.exit(app.exec_())
