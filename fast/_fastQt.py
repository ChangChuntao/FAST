# -*- coding: utf-8 -*-
# FAST           : MAIN of FAST GUI
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2022.11.09 - Version 2.01.00
# Latest Version : 2026.03.17 - Version 3.01.00

import os
import sys
from PyQt5.QtGui import QFont, QPixmap, QFontDatabase
from PyQt5.QtWidgets import QDesktopWidget, QSplitter
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QApplication, QSplashScreen
from fast.qt.qtFrame import FramelessWindow, getSetting
from fast.com.pub import lastVersion, lastVersionTime
import qdarkstyle
import pkg_resources

if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
else:
    dirname = os.path.dirname(os.path.abspath(__file__))

style_path = pkg_resources.resource_filename(__name__, 'qb-common.mplstyle')
if os.path.isdir(os.path.join(dirname, 'win_bin')):
    binDir = os.path.join(dirname, 'win_bin')
else:
    binDir = os.path.join(dirname, 'mac_bin')

ttf_dir = os.path.join(binDir, 'ttf')


class mainWindow(QMainWindow):
    move_Flag = False
    global self

    def __init__(self, fastQtSetting):
        super().__init__()
        self.fastQtSetting = fastQtSetting
        self.initUI()

    def initUI(self):
        # 导入UI初始化函数
        from fast.qt.qtInitUI import (
            init_time_ui, init_download_ui, init_qc_ui,
            init_spp_ui, init_site_ui, init_main_tabs
        )
        from qbstyles import mpl_style
        
        # 获取屏幕尺寸
        screen = QDesktopWidget().screenGeometry()
        screenWidth = screen.width()
        screenHeight = screen.height()

        # 计算尺寸参数
        lable_size = int(screenWidth / 9)
        lable_h = int(screenHeight / 48)
        choose_size = int(screenWidth / 6.5)
        choose_h = int(screenHeight / 100)
        tab_h = int(screenHeight / 50)
        normalBtnSize = int(screenWidth / 20)
        normalBtnH = int(screenHeight / 36)

        # 设置字体
        font = QtGui.QFont()
        ttf_path = os.path.join(ttf_dir, self.fastQtSetting['ttf'])
        font_id = QFontDatabase.addApplicationFont(ttf_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        default_font = QFont(font_family)
        default_font.setPointSize(10)
        QApplication.setFont(default_font)

        # 设置绘图样式
        if self.fastQtSetting['plotBackgroundColor'] == 'dark':
            mpl_style(dark=True)
        else:
            mpl_style(dark=False)

        # 语言设置
        if self.fastQtSetting['language'] == 'CHN':
            self.chinese = True
        else:
            self.chinese = False

        self.savePngDPI = self.fastQtSetting['savePngDPI']
        self.exeDirName = dirname

        # 状态栏
        self.status = self.statusBar()
        self.status.showMessage("GNSS Center, WHU")
        self.showName = QLabel("Author:Chuntao Chang")
        self.showName.setFont(font)
        self.status.addPermanentWidget(self.showName, stretch=0)

        # 大字体
        font_big = QtGui.QFont()
        font_big.setPointSize(10)
        font_big.setBold(True)

        # 初始化各模块UI
        # 时间转换模块
        splitterLeft = init_time_ui(self, font, self.chinese, normalBtnSize, normalBtnH)

        # 下载模块
        splitterRight = init_download_ui(
            self, font, font_big, self.chinese, lable_size, lable_h,
            choose_size, choose_h, normalBtnSize, normalBtnH, lastVersion, lastVersionTime
        )

        # 下载模块布局
        splitterAll = QSplitter(Qt.Horizontal)
        splitterAll.addWidget(splitterLeft)
        splitterAll.addWidget(splitterRight)
        splitterAll.setSizes([10, 80])
        downloadLayout = QHBoxLayout(self)
        downloadLayout.addWidget(splitterAll)

        # QC模块
        qcLayout = init_qc_ui(self, font, self.chinese, choose_h, screenWidth, screenHeight)

        # SPP模块
        sppLayout = init_spp_ui(self, font, self.chinese, choose_h)

        # Site模块
        siteLayout = init_site_ui(self, font, self.chinese, lable_h, normalBtnH)

        # 主Tab布局
        init_main_tabs(self, font, self.chinese, downloadLayout, qcLayout, sppLayout, siteLayout)


# 延迟导入以避免循环导入
from PyQt5.QtWidgets import QLabel


def fastAppMain():
    fastApp = QApplication(sys.argv)
    whuLoadPng = os.path.join(binDir, 'black_2_1.png')
    splash_pix = QPixmap(whuLoadPng)
    target_size = QSize(800, 400)
    splash_pix = splash_pix.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    fastApp.setStyleSheet(qdarkstyle.load_stylesheet())

    framelessWnd = FramelessWindow()
    whu_ico = os.path.join(binDir, 'black_c.ico')
    framelessWnd.setWindowIcon(QtGui.QIcon(whu_ico))
    framelessWnd.setWindowTitle('FAST V' + lastVersion)

    settingFile = os.path.join(binDir, 'setting')
    fastQtSetting = getSetting(settingFile)
    win = mainWindow(fastQtSetting)
    framelessWnd.setContent(win)
    splash.close()
    framelessWnd.show()
    sys.exit(fastApp.exec())


if __name__ == '__main__':
    fastAppMain()