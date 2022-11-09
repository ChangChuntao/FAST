import platform
from PyQt5.QtCore import pyqtSignal
from PyQt5 import QtCore, QtGui
from PyQt5.QtCore import Qt, QEvent, QRect, QPoint
from PyQt5.QtGui import QIcon, QScreen, QColor, QPalette, QGuiApplication
from PyQt5.QtWidgets import (QWidget, QApplication, QDesktopWidget, QGraphicsDropShadowEffect,
                             QHBoxLayout, QVBoxLayout, QLabel, QToolButton, QSizePolicy, qApp)
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle


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



CONST_DRAG_BORDER_SIZE = 15


class FramelessWindow(QWidget):

    def __init__(self, parent=None):
        super(FramelessWindow, self).__init__(parent)

        self.mousePressed = False
        self.dragTop = False
        self.dragLeft = False
        self.dragRight = False
        self.dragBottom = False
        self.startGeometry = QRect()

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowSystemMenuHint)
        # 为了在Windows系统下正确处理最小化函数，需要加上最小化标志按钮
        if platform.system() == 'Windows':
            self.setWindowFlags(self.windowFlags() | Qt.WindowMinimizeButtonHint)

        self.setAttribute(Qt.WA_NoSystemBackground, True)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.initUi()

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

        # 关闭按钮
        self.btnClose = QToolButton()
        self.btnClose.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnClose.setIcon(QIcon('./win_bin/close-we.png'))
        self.btnClose.clicked.connect(self.close)
        # 最大化按钮
        self.btnMaximize = QToolButton()
        self.btnMaximize.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnMaximize.setIcon(QIcon('./win_bin/max-we.png'))
        self.btnMaximize.clicked.connect(self.onButtonMaximizeClicked)
        # 最小化按钮
        self.btnMinimize = QToolButton()
        self.btnMinimize.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnMinimize.setIcon(QIcon('./win_bin/min-we.png'))
        self.btnMinimize.clicked.connect(lambda: self.setWindowState(Qt.WindowMinimized))
        # 恢复按钮
        self.btnRestore = QToolButton()
        self.btnRestore.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.btnRestore.setIcon(QIcon('./win_bin/restore-we.png'))
        self.btnRestore.clicked.connect(self.onButtonRestoreClicked)

        # 做边留空
        spacer = QLabel()
        spacer.setFixedWidth(4)
        # 左上角应用图标
        self.icon = QLabel()
        self.icon.setFixedSize(60, 60)
        # 中间标题信息
        self.titleText = QLabel()
        self.titleText.setStyleSheet('border: 0px none palette(base);')

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
        font.setFamily('Microsoft YaHei')
        font.setPointSize(9)
        self.titleText.setFont(font)


    def setWindowIcon(self, ico):
        self.icon.setPixmap(ico.pixmap(30, 35))
        self.icon.setMinimumSize(30, 35)

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

        # 当鼠标在对象上移动时，检查鼠标移动事件
        if event.type() == QEvent.MouseMove and event:
            self.checkBorderDragging(event)
            # 只有在frame window上时，才触发按下事件
        elif event.type() == QEvent.MouseButtonPress and watched is self:
            if event:
                self.mousePressEvent(event)
        elif event.type() == QEvent.MouseButtonRelease:
            if self.mousePressed and event:
                self.mouseReleaseEvent(event)

        return QWidget.eventFilter(self, watched, event)
