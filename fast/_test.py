import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QDesktopWidget
from PyQt5.QtCore import QRect

class CenterWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        self.setWindowTitle('Centered Window')
        self.setGeometry(0, 0, 400, 300)  # 设置窗口初始大小

        # 计算屏幕中心点
        screen = QDesktopWidget().screenGeometry()
        screen_center = screen.center()

        # 计算窗口左上角点
        window_rect = self.frameGeometry()
        window_rect.moveCenter(screen_center)
        self.move(window_rect.topLeft())

if __name__ == '__main__':
    app = QApplication(sys.argv)
    mainWindow = CenterWindow()
    mainWindow.show()
    sys.exit(app.exec_())
