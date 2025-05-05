# -*- coding: utf-8 -*-
# qtQc              : pyqt5 for FAST
# Author            : Chang Chuntao
# Copyright(C)      : The GNSS Center, Wuhan University
# Latest Version    : 3.00.02
# Creation Date     : 2023.10.05 - Version 3.00.00
# Date              : 2024.07.01 - Version 3.00.02

import platform
from PyQt5.QtCore import pyqtSignal, QSize
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QEvent, QRect, QPoint
from PyQt5.QtGui import QIcon, QScreen, QColor, QPalette, QGuiApplication
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QGraphicsDropShadowEffect,
                             QHBoxLayout, QVBoxLayout, QLabel, QToolButton, QSizePolicy)
from PyQt5.QtGui import QPainter, QCursor
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle, QLineEdit, QListWidget, QCheckBox, QListWidgetItem, QAbstractItemView
import sys, os
from PyQt5.QtWidgets import QComboBox

if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
else:
    dirname = os.path.dirname(os.path.abspath(__file__))
    dirname = os.path.join(dirname, '..')

if os.path.isdir(os.path.join(dirname, 'win_bin')):
    binDir = os.path.join(dirname, 'win_bin')
else:
    binDir = os.path.join(dirname, 'mac_bin')

class WindowDragger(QWidget):
    doubleClicked = pyqtSignal()

    def __init__(self, parent=None):
        super(WindowDragger, self).__init__(parent)

        self.mousePressed = False

    def mousePressEvent(self, event):
        self.mousePressed = True
        self.mousePos = event.globalPos()

        parent = self.parentWidget()
        if parent:
            parent = parent.parentWidget()

        if parent:
            self.wndPos = parent.pos()

    def mouseMoveEvent(self, event):
        parent = self.parentWidget()
        if parent:
            parent = parent.parentWidget()

        if parent and self.mousePressed:
            parent.move(self.wndPos + (event.globalPos() - self.mousePos))

    def mouseReleaseEvent(self, event):
        self.mousePressed = False

    def mouseDoubleClickEvent(self, event):
        self.doubleClicked.emit()

    def paintEvent(self, event):
        styleOption = QStyleOption()
        styleOption.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, styleOption, painter, self)


CONST_DRAG_BORDER_SIZE = 10


class FramelessWindow(QWidget):

    def __init__(self, parent=None):
        super(FramelessWindow, self).__init__(parent)

        self.mousePressed = False
        self.dragTop = False
        self.dragLeft = False
        self.dragRight = False
        self.dragBottom = False
        self.startGeometry = QRect()
        # self.resize(500, 500)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        # 为了在Windows系统下正确处理最小化函数,需要加上最小化标志按钮
        if platform.system() == 'Windows':
            self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)

        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.initUi()
        self.center()  # 将窗口居中显示

        # 窗口阴影
        windowShadow = QGraphicsDropShadowEffect()
        windowShadow.setBlurRadius(9.0)
        windowShadow.setColor(self.palette().color(QPalette.Highlight))
        windowShadow.setOffset(0.0)
        self.windowFrame.setGraphicsEffect(windowShadow)

        self.setMouseTracking(True)

        # 监测所有子窗口的鼠标移动事件
        QApplication.instance().installEventFilter(self)

    def initUi(self):
        
        screen = QDesktopWidget().screenGeometry()
        screenWidth = screen.width()
        screenHeight = screen.height()

        # 关闭按钮
        # self.resize(800, 600)
        self.btnClose = QToolButton()
        self.btnClose.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnClose.setFixedSize(int(screenHeight/45), int(screenHeight/45))
        close_png = os.path.join(binDir, 'close-we.png')
        self.btnClose.setIcon(QIcon(close_png))
        self.btnClose.clicked.connect(self.close)
        # 最大化按钮
        self.btnMaximize = QToolButton()
        self.btnMaximize.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnMaximize.setFixedSize(int(screenHeight/45), int(screenHeight/45))
        max_png = os.path.join(binDir, 'max-we.png')
        self.btnMaximize.setIcon(QIcon(max_png))
        self.btnMaximize.clicked.connect(self.onButtonMaximizeClicked)
        # 最小化按钮
        self.btnMinimize = QToolButton()
        self.btnMinimize.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnMinimize.setFixedSize(int(screenHeight/45), int(screenHeight/45))
        min_png = os.path.join(binDir, 'min-we.png')
        self.btnMinimize.setIcon(QIcon(min_png))
        self.btnMinimize.clicked.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        # 恢复按钮
        self.btnRestore = QToolButton()
        self.btnRestore.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnRestore.setFixedSize(int(screenHeight/45), int(screenHeight/45))
        restore_png = os.path.join(binDir, 'restore-we.png')
        self.btnRestore.setIcon(QIcon(restore_png))
        self.btnRestore.clicked.connect(self.onButtonRestoreClicked)

        # 做边留空
        spacer = QLabel()
        spacer.setFixedWidth(int(screenHeight/350))
        # 左上角应用图标
        self.icon = QLabel()
        self.icon.setFixedSize(int(screenHeight/30), int(screenHeight/30))
        # 中间标题信息
        self.titleText = QLabel()
        self.titleText.setStyleSheet('border: 0px none palette(base);')
        self.titleText.setFixedHeight(int(screenHeight/30))  # 设置高度为 50 像素

        # 标题条布局
        layoutTitlebar = QHBoxLayout()
        layoutTitlebar.setContentsMargins(1, 1, 1, 1)
        layoutTitlebar.setSpacing(0)
        layoutTitlebar.addWidget(spacer)
        layoutTitlebar.addWidget(self.icon)
        layoutTitlebar.addWidget(self.titleText)
        layoutTitlebar.addWidget(self.btnMinimize)
        layoutTitlebar.addWidget(self.btnRestore)
        layoutTitlebar.addWidget(self.btnMaximize)
        layoutTitlebar.addWidget(self.btnClose)
        layoutTitlebar.addWidget(spacer)

        self.windowTitlebar = WindowDragger()
        self.windowTitlebar.setLayout(layoutTitlebar)
        self.windowTitlebar.doubleClicked.connect(self.titlebarDoubleClicked)

        # 窗口内容部分
        contentLayout = QVBoxLayout()
        contentLayout.setContentsMargins(0, 0, 0, 0)
        contentLayout.setSpacing(0)
        self.windowContent = QWidget()
        self.windowContent.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        self.windowContent.setLayout(contentLayout)

        self.windowFrame = QWidget(self)
        frameLayout = QVBoxLayout()
        frameLayout.setContentsMargins(0, 0, 0, 0)
        frameLayout.setSpacing(0)
        frameLayout.addWidget(self.windowTitlebar)
        frameLayout.addWidget(self.windowContent)
        self.windowFrame.setLayout(frameLayout)

        # 设置整个窗口的布局
        layout = QVBoxLayout(self)
        layout.setContentsMargins(10, 10, 10, 10)
        # layout.setSpacing(0)
        layout.addWidget(self.windowFrame)
        self.setLayout(layout)

        self.btnRestore.setVisible(False)

    def onButtonRestoreClicked(self):
        self.btnRestore.setVisible(False)
        self.btnMaximize.setVisible(True)
        self.layout().setContentsMargins(10, 10, 10, 10)
        self.setWindowState(Qt.WindowNoState)
        self.showNormal()

    def onButtonMaximizeClicked(self):
        self.btnMaximize.setVisible(False)
        self.btnRestore.setVisible(True)
        self.layout().setContentsMargins(0, 0, 0, 0)
        self.setWindowState(Qt.WindowMaximized)
        self.showMaximized()

    def setContent(self, widget):
        self.windowContent.layout().addWidget(widget)

    def setWindowTitle(self, text):
        self.titleText.setText(text)
        font = QtGui.QFont()
        font.setBold(True)
        # font.setFamily('Microsoft YaHei')
        font.setPointSize(11)
        self.titleText.setFont(font)

    def center(self):
        self.move(100,100)
        
    def setWindowIcon(self, ico):
        # self.icon.setPixmap(ico.pixmap(30, 35))
        # self.icon.setMinimumSize(30, 35)

        self.icon.setPixmap(ico.pixmap(30, 30))
        # self.icon.setMinimumSize(40, 40)
        self.icon.setAlignment(Qt.AlignVCenter)
        super(FramelessWindow, self).setWindowIcon(ico)

    def titlebarDoubleClicked(self):
        if self.isMaximized():
            self.onButtonRestoreClicked()
        else:
            self.onButtonMaximizeClicked()

    def mouseDoubleClickEvent(self, event):
        pass

    def checkBorderDragging(self, event):
        if self.isMaximized():
            return

        globalMousePos = event.globalPos()
        if self.mousePressed:
            screen = QGuiApplication.primaryScreen()
            # 除开任务栏外可用的空间
            availGeometry = screen.availableGeometry()
            h = availGeometry.height()
            w = availGeometry.width()
            screenList = screen.virtualSiblings()
            if screen in screenList:
                sz = QApplication.desktop().size()
                h = sz.height()
                w = sz.width()

            # 右上角
            if self.dragTop and self.dragRight:
                new_w = globalMousePos.x() - self.startGeometry.x()
                new_y = globalMousePos.y()
                if new_w > 0 and new_y > 0 and new_y < h - 50:
                    new_geom = self.startGeometry
                    new_geom.setWidth(new_w)
                    new_geom.setX(self.startGeometry.x())
                    new_geom.setY(new_y)
                    self.setGeometry(new_geom)
                    # 左上角
            elif self.dragTop and self.dragLeft:
                new_x = globalMousePos.x()
                new_y = globalMousePos.y()
                if new_x > 0 and new_y > 0:
                    new_geom = self.startGeometry
                    new_geom.setX(new_x)
                    new_geom.setY(new_y)
                    self.setGeometry(new_geom)
                    # 左下角
            elif self.dragBottom and self.dragLeft:
                new_h = globalMousePos.y() - self.startGeometry.y()
                new_x = globalMousePos.x()
                if new_h > 0 and new_x > 0:
                    new_geom = self.startGeometry
                    new_geom.setX(new_x)
                    new_geom.setHeight(new_h)
                    self.setGeometry(new_geom)
            elif self.dragTop:
                new_y = globalMousePos.y()
                if new_y > 0 and new_y < h - 50:
                    new_geom = self.startGeometry
                    new_geom.setY(new_y)
                    self.setGeometry(new_geom)
            elif self.dragLeft:
                new_x = globalMousePos.x()
                if new_x > 0 and new_x < w - 50:
                    new_geom = self.startGeometry
                    new_geom.setX(new_x)
                    self.setGeometry(new_geom)
            elif self.dragRight:
                new_w = globalMousePos.x() - self.startGeometry.x()
                if new_w > 0:
                    new_geom = self.startGeometry
                    new_geom.setWidth(new_w)
                    new_geom.setX(self.startGeometry.x())
                    self.setGeometry(new_geom)
            elif self.dragBottom:
                new_h = globalMousePos.y() - self.startGeometry.y()
                if new_h > 0:
                    new_geom = self.startGeometry
                    new_geom.setHeight(new_h)
                    new_geom.setY(self.startGeometry.y())
                    self.setGeometry(new_geom)
        else:
            # 没有鼠标按下
            if self.leftBorderHit(globalMousePos) and self.topBorderHit(globalMousePos):
                self.setCursor(Qt.SizeFDiagCursor)
            elif self.rightBorderHit(globalMousePos) and self.topBorderHit(globalMousePos):
                self.setCursor(Qt.SizeBDiagCursor)
            elif self.leftBorderHit(globalMousePos) and self.bottomBorderHit(globalMousePos):
                self.setCursor(Qt.SizeBDiagCursor)
            else:
                if self.topBorderHit(globalMousePos):
                    self.setCursor(Qt.SizeVerCursor)
                elif self.leftBorderHit(globalMousePos):
                    self.setCursor(Qt.SizeHorCursor)
                elif self.rightBorderHit(globalMousePos):
                    self.setCursor(Qt.SizeHorCursor)
                elif self.bottomBorderHit(globalMousePos):
                    self.setCursor(Qt.SizeVerCursor)
                else:
                    self.dragTop = False
                    self.dragLeft = False
                    self.dragRight = False
                    self.dragBottom = False
                    self.setCursor(Qt.ArrowCursor)

    def leftBorderHit(self, pos):
        rect = self.geometry()
        if pos.x() >= rect.x() and pos.x() <= (rect.x() + CONST_DRAG_BORDER_SIZE):
            return True
        return False

    def rightBorderHit(self, pos):
        rect = self.geometry()
        tmp = rect.x() + rect.width()
        if pos.x() <= tmp and pos.x() >= (tmp - CONST_DRAG_BORDER_SIZE):
            return True
        return False

    def topBorderHit(self, pos):
        rect = self.geometry()
        if pos.y() >= rect.y() and pos.y() <= (rect.y() + CONST_DRAG_BORDER_SIZE):
            return True
        return False

    def bottomBorderHit(self, pos):
        rect = self.geometry()
        tmp = rect.y() + rect.height()
        if pos.y() <= tmp and pos.y() >= (tmp - CONST_DRAG_BORDER_SIZE):
            return True
        return False

    def mousePressEvent(self, event):
        if self.isMaximized():
            return

        self.mousePressed = True
        self.startGeometry = self.geometry()

        globalMousePos = self.mapToGlobal(QPoint(event.x(), event.y()))

        if self.leftBorderHit(globalMousePos) and self.topBorderHit(globalMousePos):
            self.dragTop = True
            self.dragLeft = True
            self.setCursor(Qt.SizeFDiagCursor)
        elif self.rightBorderHit(globalMousePos) and self.topBorderHit(globalMousePos):
            self.dragTop = True
            self.dragRight = True
            self.setCursor(Qt.SizeBDiagCursor)
        elif self.leftBorderHit(globalMousePos) and self.bottomBorderHit(globalMousePos):
            self.dragLeft = True
            self.dragBottom = True
            self.setCursor(Qt.SizeBDiagCursor)
        else:
            if self.topBorderHit(globalMousePos):
                self.dragTop = True
                self.setCursor(Qt.SizeVerCursor)
            elif self.leftBorderHit(globalMousePos):
                self.dragLeft = True
                self.setCursor(Qt.SizeHorCursor)
            elif self.rightBorderHit(globalMousePos):
                self.dragRight = True
                self.setCursor(Qt.SizeHorCursor)
            elif self.bottomBorderHit(globalMousePos):
                self.dragBottom = True
                self.setCursor(Qt.SizeVerCursor)

    def mouseReleaseEvent(self, event):
        if self.isMaximized():
            return

        self.mousePressed = False
        switchBackCursorNeeded = self.dragTop and self.dragLeft and self.dragRight and self.dragBottom
        self.dragTop = False
        self.dragLeft = False
        self.dragRight = False
        self.dragBottom = False
        if switchBackCursorNeeded:
            self.setCursor(Qt.ArrowCursor)

    def eventFilter(self, watched, event):
        if self.isMaximized():
            return QWidget.eventFilter(self, watched, event)

        # 当鼠标在对象上移动时,检查鼠标移动事件
        if event.type() == QEvent.MouseMove and event:
            self.checkBorderDragging(event)
            # 只有在frame window上时,才触发按下事件
        elif event.type() == QEvent.MouseButtonPress and watched is self:
            if event:
                self.mousePressEvent(event)
        elif event.type() == QEvent.MouseButtonRelease:
            if self.mousePressed and event:
                self.mouseReleaseEvent(event)

        return QWidget.eventFilter(self, watched, event)

class ComboLineEdit(QLineEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.textChanged.connect(self.checkText)
        self.clearTriggered = False

    def checkText(self):
        if not self.text() and not self.hasFocus() and not self.clearTriggered:
            self.setText(self.originalText)
        if len(self.text()) > 0:
            self.originalText = self.text()

    def focusInEvent(self, event):
        self.originalText = self.text()
        super().focusInEvent(event)

    def clearText(self):
        self.clearTriggered = True
        self.clear()
        self.clearTriggered = False


class ComboCheckBox(QComboBox):
    def __init__(self, items, chooseNum):  # items==[str,str...]
        super(ComboCheckBox, self).__init__()
        if not items:
            items = ['']
        self.items = items
        self.qCheckBox = []
        self.qLineEdit = ComboLineEdit()
        self.qLineEdit.setReadOnly(True)
        
        self.qListWidget = QListWidget()
        self.chooseNum = chooseNum
        self.row_num = len(self.items)
        self.onItemClicked = False

        # 添加“全选/全不选”复选框
        self.selectAll = QCheckBox("Select All")
        self.qListWidget.insertItem(0, QListWidgetItem())
        self.qListWidget.setItemWidget(self.qListWidget.item(0), self.selectAll)
        self.selectAll.stateChanged.connect(self.selectAllOrNone)
        self.qListWidget.item(0).setSizeHint(QSize(0, 30))  # 设置行高为 30 像素

        for i in range(self.row_num):
            self.qCheckBox.append(QCheckBox())
            qItem = QListWidgetItem(self.qListWidget)
            self.qCheckBox[i].setText(self.items[i])
            self.qListWidget.setItemWidget(qItem, self.qCheckBox[i])
            self.qCheckBox[i].stateChanged.connect(self.show)
            qItem.setSizeHint(QSize(0, 30))

        self.qCheckBox[0].setChecked(False)  # 将第一个复选框设置为未选中状态

        self.setLineEdit(self.qLineEdit)
        self.setModel(self.qListWidget.model())
        self.setView(self.qListWidget)

    def Selectlist(self):
        Outputlist = []
        for i in range(self.row_num):
            if self.qCheckBox[i].isChecked():
                Outputlist.append(self.qCheckBox[i].text())
        return Outputlist

    def show(self):
        if self.chooseNum is not None:
            if len(self.Selectlist()) > self.chooseNum:
                return 0
        show = ''
        self.qLineEdit.setReadOnly(False)
        self.qLineEdit.clearText()
        for i in self.Selectlist():
            if i != '' and i != 'Select All':
                show += i + ','
        show = show[:-1]
        self.qLineEdit.setText(show)
        self.qLineEdit.setReadOnly(True)


    def selectAllOrNone(self, state):
        for checkbox in self.qCheckBox:
            checkbox.setChecked(state != Qt.Unchecked)
            
    def clear(self):
        self.qListWidget.clear()  # 清除所有列表项
        self.qCheckBox.clear()  # 清除之前添加的复选框
        self.row_num = 0
        # 添加“全选/全不选”复选框
        self.selectAll = QCheckBox("Select All")
        self.qListWidget.insertItem(0, QListWidgetItem())
        self.qListWidget.setItemWidget(self.qListWidget.item(0), self.selectAll)
        self.selectAll.stateChanged.connect(self.selectAllOrNone)
        self.selectAll.setChecked(True)
        self.qListWidget.item(0).setSizeHint(QSize(0, 30))  # 设置行高为 30 像素

    def addItem(self, item):
        self.items.append(item)
        self.qCheckBox.append(QCheckBox())
        qItem = QListWidgetItem(self.qListWidget)
        self.qCheckBox[self.row_num].setText(item)
        self.qListWidget.setItemWidget(qItem, self.qCheckBox[self.row_num])
        self.qCheckBox[self.row_num].stateChanged.connect(self.show)
        qItem.setSizeHint(QSize(0, 30))
        self.row_num += 1
        
    def hidePopup(self):
        # 判断是否点击到了qListWidget
        if self.view().rect().contains(self.view().mapFromGlobal(QCursor.pos())):
            return
        
        self.view().scrollTo(self.model().index(self.currentIndex(), 0), QAbstractItemView.PositionAtTop)
        super(ComboCheckBox, self).hidePopup()


def getSetting(colorFile):
    colorOpen = open(colorFile, 'r+',encoding='utf-8', errors = 'ignore')
    colorLine = colorOpen.readlines()
    fastQtStyle = {}
    for line in colorLine:
        line = line.split('#')[0]
        if 'plotBackgroundColor' in line:
            fastQtStyle['plotBackgroundColor'] = line.split('=')[-1].strip()
        elif 'language' in line:
            fastQtStyle['language'] = line.split('=')[-1].strip()
        elif 'savePngDPI' in line:
            try:
                fastQtStyle['savePngDPI'] = int(line.split('=')[-1].strip())
            except:
                fastQtStyle['savePngDPI'] = 800
        elif 'ttf' in line:
            fastQtStyle['ttf'] = line.split('=')[-1].strip()
    return fastQtStyle