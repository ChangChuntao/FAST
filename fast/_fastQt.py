# -*- coding: utf-8 -*-
# FAST           : MAIN of FAST GUI
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2022.11.09 - Version 2.01.00
# Latest Version : 2025.05.05 - Version 3.00.03

import os
import sys
from PyQt5.QtGui import QFont, QPixmap, QFontDatabase
from PyQt5.QtWidgets import QGridLayout, QComboBox, QTextEdit, QTabWidget
from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QDateTime, QSize
from PyQt5.QtWidgets import QMainWindow, QHBoxLayout, QApplication, QFrame, QWidget, QSplitter, QLabel, \
    QPushButton, QLineEdit, QVBoxLayout, QDateTimeEdit, QCheckBox, QSplashScreen, QDesktopWidget
from fast.qt.qtFrame import FramelessWindow, ComboCheckBox, getSetting
from fast.qt.timeTran import time_tran, time_tran_none
from fast.com.pub import gnss_type, lastVersion, lastVersionTime
from fast.qt.qtDownload import *
from fast.qt.qtQc import analyze_plot, qcSysChange, choose_obs_and_process, batch_analyze_plot, saveQcFile
from fast.qt.qtSpp import sppChooseObsProcess, runSpp, saveSppPos, sppChooseNav
from fast.qt.qtSite import sitePlotProcess, siteChooseFileProcess, siteCombBoxChanged, saveSite
import qdarkstyle
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from qbstyles import mpl_style
import pkg_resources
# import importlib.resources as importlib_resources
import ctypes


if getattr(sys, 'frozen', False):
    dirname = os.path.dirname(sys.executable)
else:
    dirname = os.path.dirname(os.path.abspath(__file__))

style_path = pkg_resources.resource_filename(__name__, 'qb-common.mplstyle')
ttf_dir = os.path.join(dirname, 'win_bin', 'ttf')


class mainWindow(QMainWindow):
    move_Flag = False
    global self

    def __init__(self, fastQtSetting):
        super().__init__()  # 继承类
        
    
        self.fastQtSetting = fastQtSetting
        self.initUI()

    def initUI(self):
        global font
        # get screen size
        screen = QDesktopWidget().screenGeometry()
        screenWidth = screen.width()
        screenHeight = screen.height()
        window_size = self.size()
        window_width = window_size.width()  # 获取窗口的宽度
        window_height = window_size.height()  # 获取窗口的高度
        print(window_width, window_height)

        # init size
        lable_size = int(screenWidth/9)
        lable_h = int(screenHeight/48)
        choose_size = int(screenWidth/6.5)
        choose_h = int(screenHeight/100)
        tab_h = int(screenHeight/50)
        normalBtnSize = int(screenWidth/20)
        normalBtnH = int(screenHeight/36)
        lable_size_siteTab = int(screenWidth/9)

        font = QtGui.QFont()
        # font.setPointSize(8)
        # font.setPointSize(int(screenWidth/270))
        ttf_path = os.path.join(ttf_dir, self.fastQtSetting['ttf'])
        font_id = QFontDatabase.addApplicationFont(ttf_path)
        font_family = QFontDatabase.applicationFontFamilies(font_id)[0]
        default_font = QFont(font_family)
        default_font.setPointSize(10)
        QApplication.setFont(default_font)


        if self.fastQtSetting['plotBackgroundColor'] == 'dark':
            mpl_style(dark=True)
        else:
            mpl_style(dark=False)

        if self.fastQtSetting['language'] == 'CHN':
            self.chinese = True
        else:
            self.chinese = False
        
        self.savePngDPI = self.fastQtSetting['savePngDPI']
        
        self.exeDirName = dirname

        # ------------------标题栏-------------------
        self.status = self.statusBar()
        self.status.showMessage("GNSS Center, WHU")
        self.showName = QLabel("Author:Chuntao Chang")
        self.showName.setFont(font)
        self.showEmail = QLabel("Email:chuntaochang@whu.edu.cn")
        self.showEmail.setFont(font)

        self.status.addPermanentWidget(self.showName, stretch=0)  # 比例
        # self.status.addPermanentWidget(self.showEmail, stretch=0)
        # ------------------标题栏-------------------

        # ----------------左侧控件布局----------------
        datetime_Label_box = QHBoxLayout()
        datetime_Label = QLabel("GPS Datetime")
        datetime_Label.setFont(font)
        datetime_Label.setAlignment(Qt.AlignCenter)
        datetime_Label_box.addWidget(datetime_Label)
        datetime_Label_wg = QWidget()
        datetime_Label_wg.setLayout(datetime_Label_box)

        dateTimeEdit_box = QHBoxLayout()
        self.dateTimeEdit = QDateTimeEdit()
        self.dateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
        self.dateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
        self.dateTimeEdit.setFont(font)
        dateTimeEdit_box.addWidget(self.dateTimeEdit)
        dateTimeEdit_wg = QWidget()
        dateTimeEdit_wg.setLayout(dateTimeEdit_box)

        year_Label_box = QHBoxLayout()
        year_Label = QLabel("Year")
        year_Label.setAlignment(Qt.AlignCenter)
        year_Label.setFont(font)
        month_Label = QLabel("Month")
        month_Label.setFont(font)
        month_Label.setAlignment(Qt.AlignCenter)
        day_Label = QLabel("Day")
        day_Label.setFont(font)
        day_Label.setAlignment(Qt.AlignCenter)
        year_Label_box.addWidget(year_Label)
        year_Label_box.addWidget(month_Label)
        year_Label_box.addWidget(day_Label)
        year_Label_wg = QWidget()
        year_Label_wg.setLayout(year_Label_box)

        ymd_box = QHBoxLayout()
        self.year_text = QLineEdit(self)
        self.year_text.setFont(font)
        self.year_text.setAlignment(Qt.AlignCenter)
        self.month_text = QLineEdit(self)
        self.month_text.setFont(font)
        self.month_text.setAlignment(Qt.AlignCenter)
        self.day_text = QLineEdit(self)
        self.day_text.setAlignment(Qt.AlignCenter)
        self.day_text.setFont(font)
        ymd_box.addWidget(self.year_text)
        ymd_box.addWidget(self.month_text)
        ymd_box.addWidget(self.day_text)
        ymd_wg = QWidget()
        ymd_wg.setLayout(ymd_box)

        ydoy_Label_box = QHBoxLayout()
        ydoy_Label = QLabel("Year")
        ydoy_Label.setFont(font)
        ydoy_Label.setAlignment(Qt.AlignCenter)
        doy_Label = QLabel("Doy")
        doy_Label.setFont(font)
        doy_Label.setAlignment(Qt.AlignCenter)
        ydoy_Label_box.addWidget(ydoy_Label)
        ydoy_Label_box.addWidget(doy_Label)
        ydoy_Label_wg = QWidget()
        ydoy_Label_wg.setLayout(ydoy_Label_box)

        ydoy_box = QHBoxLayout()
        self.yearofdoy_text = QLineEdit(self)
        self.yearofdoy_text.setFont(font)
        self.yearofdoy_text.setAlignment(Qt.AlignCenter)
        self.doy_text = QLineEdit(self)
        self.doy_text.setFont(font)
        self.doy_text.setAlignment(Qt.AlignCenter)
        ydoy_box.addWidget(self.yearofdoy_text)
        ydoy_box.addWidget(self.doy_text)
        ydoy_wg = QWidget()
        ydoy_wg.setLayout(ydoy_box)

        gpsweekd_Label_box = QHBoxLayout()
        gpsweek_Label = QLabel("GPS Week")
        gpsweek_Label.setFont(font)
        gpsweek_Label.setAlignment(Qt.AlignCenter)
        gps_dow_Label = QLabel("Day of Week")
        gps_dow_Label.setFont(font)
        gps_dow_Label.setAlignment(Qt.AlignCenter)
        gpsweekd_Label_box.addWidget(gpsweek_Label)
        gpsweekd_Label_box.addWidget(gps_dow_Label)
        gpsweekd_Label_wg = QWidget()
        gpsweekd_Label_wg.setLayout(gpsweekd_Label_box)

        gpsweekd_box = QHBoxLayout()
        self.gpsweek_text = QLineEdit(self)
        self.gpsweek_text.setFont(font)
        self.gpsweek_text.setAlignment(Qt.AlignCenter)
        self.gpsdow_text = QLineEdit(self)
        self.gpsdow_text.setFont(font)
        self.gpsdow_text.setAlignment(Qt.AlignCenter)
        gpsweekd_box.addWidget(self.gpsweek_text)
        gpsweekd_box.addWidget(self.gpsdow_text)
        gpsweekd_wg = QWidget()
        gpsweekd_wg.setLayout(gpsweekd_box)

        bdsweekd_Label_box = QHBoxLayout()
        bdsweek_Label = QLabel("BDS week")
        bdsweek_Label.setFont(font)
        bdsweek_Label.setAlignment(Qt.AlignCenter)
        bds_dow_Label = QLabel("Day of Week")
        bds_dow_Label.setFont(font)
        bds_dow_Label.setAlignment(Qt.AlignCenter)
        bdsweekd_Label_box.addWidget(bdsweek_Label)
        bdsweekd_Label_box.addWidget(bds_dow_Label)
        bdsweekd_Label_wg = QWidget()
        bdsweekd_Label_wg.setLayout(bdsweekd_Label_box)

        bdsweekd_box = QHBoxLayout()
        self.bdsweek_text = QLineEdit(self)
        self.bdsweek_text.setFont(font)
        self.bdsweek_text.setAlignment(Qt.AlignCenter)
        self.bdsdow_text = QLineEdit(self)
        self.bdsdow_text.setFont(font)
        self.bdsdow_text.setAlignment(Qt.AlignCenter)
        bdsweekd_box.addWidget(self.bdsweek_text)
        bdsweekd_box.addWidget(self.bdsdow_text)
        bdsweekd_wg = QWidget()
        bdsweekd_wg.setLayout(bdsweekd_box)

        mjdsod_Label_box = QHBoxLayout()
        mjd_Label = QLabel("MJD")
        mjd_Label.setFont(font)
        mjd_Label.setAlignment(Qt.AlignCenter)
        sod_Label = QLabel("SOD")
        sod_Label.setFont(font)
        sod_Label.setAlignment(Qt.AlignCenter)
        mjdsod_Label_box.addWidget(mjd_Label)
        mjdsod_Label_box.addWidget(sod_Label)
        mjdsod_Label_wg = QWidget()
        mjdsod_Label_wg.setLayout(mjdsod_Label_box)

        none_Label_box = QHBoxLayout()
        none_Label = QLabel("")
        none_Label_box.addWidget(none_Label)
        none_Label_wg = QWidget()
        none_Label_wg.setLayout(none_Label_box)

        mjdsod_box = QHBoxLayout()
        self.mjd_text = QLineEdit(self)
        self.mjd_text.setAlignment(Qt.AlignCenter)
        self.mjd_text.setFont(font)
        self.sod_text = QLineEdit(self)
        self.sod_text.setAlignment(Qt.AlignCenter)
        self.sod_text.setFont(font)
        mjdsod_box.addWidget(self.mjd_text)
        mjdsod_box.addWidget(self.sod_text)
        mjdsod_wg = QWidget()
        mjdsod_wg.setLayout(mjdsod_box)

        time_tran_box = QHBoxLayout()
        if self.chinese:
            time_tran_btn = QPushButton('转换', self)
        else:
            time_tran_btn = QPushButton('TRANS', self)
        time_tran_btn.setFont(font)
        time_tran_btn.setMinimumSize(QSize(normalBtnSize, normalBtnH))
        time_tran_btn.clicked.connect(lambda: time_tran(self))

        if self.chinese:
            time_tran_none_btn = QPushButton('清空', self)
        else:
            time_tran_none_btn = QPushButton('CLEAR', self)
            
        time_tran_none_btn.setFont(font)
        time_tran_none_btn.setMinimumSize(QSize(normalBtnSize, normalBtnH))
        time_tran_none_btn.clicked.connect(lambda: time_tran_none(self))

        time_tran_box.addWidget(time_tran_btn)
        time_tran_box.addWidget(time_tran_none_btn)
        time_tran_wg = QWidget()
        time_tran_wg.setLayout(time_tran_box)

        gnss_time_box = QVBoxLayout()
        gnss_time_box.setSpacing(0)
        gnss_time_box.addStretch(0)
        gnss_time_box.addWidget(datetime_Label_wg)
        gnss_time_box.addWidget(dateTimeEdit_wg)
        gnss_time_box.addWidget(year_Label_wg)
        gnss_time_box.addWidget(ymd_wg)
        gnss_time_box.addWidget(ydoy_Label_wg)
        gnss_time_box.addWidget(ydoy_wg)
        gnss_time_box.addWidget(gpsweekd_Label_wg)
        gnss_time_box.addWidget(gpsweekd_wg)
        gnss_time_box.addWidget(bdsweekd_Label_wg)
        gnss_time_box.addWidget(bdsweekd_wg)
        gnss_time_box.addWidget(mjdsod_Label_wg)
        gnss_time_box.addWidget(mjdsod_wg)

        gnss_time_box.addStretch(10)
        gnss_time_box.addWidget(none_Label_wg)
        gnss_time_box.addWidget(none_Label_wg)
        gnss_time_box.addWidget(none_Label_wg)
        gnss_time_box.addWidget(time_tran_wg)

        splitterLeft_in = QFrame()
        splitterLeft_in.setFrameShape(QFrame.StyledPanel)
        splitterLeft_in.setLayout(gnss_time_box)

        # 添加到左侧控件布局
        splitterLeft = QSplitter(Qt.Vertical)
        splitterLeft.addWidget(splitterLeft_in)

        # ----------------左侧控件布局----------------

        # ----------------右侧控件布局----------------
        # |--数据下载 -> 右侧上方
        type_choose_lay = QGridLayout()
        type_choose_lay.setSpacing(20)

        if self.chinese:
            data_type_lable = QLabel('数据类型')
        else:
            data_type_lable = QLabel('Type')
        data_type_lable.setFont(font)
        data_type_lable.setAlignment(Qt.AlignRight)
        # data_type_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(data_type_lable, 1, 0)

        self.data_type_combo = QComboBox(self)
        for gt in gnss_type:
            self.data_type_combo.addItem(gt[0])
        self.data_type_combo.setFont(font)
        self.data_type_combo.textActivated[str].connect(lambda: dataTypeOnActivated(self))
        # self.data_type_combo.setMinimumSize(QSize(choose_size, choose_h + 20))
        type_choose_lay.addWidget(self.data_type_combo, 1, 1, 1, 2)
        
        if self.chinese:
            name_type_lable = QLabel('数据名称')
        else:
            name_type_lable = QLabel('Name')
        name_type_lable.setFont(font)
        name_type_lable.setAlignment(Qt.AlignRight)
        # name_type_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(name_type_lable, 1, 3)

        self.name_type_combo = QComboBox(self)
        self.name_type_combo.clear()
        for gt2 in gnss_type[0][1]:
            self.name_type_combo.addItem(gt2)
        self.name_type_combo.setFont(font)
        # self.name_type_combo.setMinimumSize(QSize(choose_size, choose_h + 20))
        self.name_type_combo.textActivated[str].connect(lambda: nameTypeOnActivated(self))
        type_choose_lay.addWidget(self.name_type_combo, 1, 4, 1, 2)


        if self.chinese:
            year_lable = QLabel('下载年份')
        else:
            year_lable = QLabel('Year')
        year_lable.setFont(font)
        year_lable.setAlignment(Qt.AlignRight)
        # year_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(year_lable, 2, 0)

        self.year_line = QLineEdit(self)
        self.year_line.setFont(font)
        # self.year_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.year_line, 2, 1, 1, 2)


        if self.chinese:
            month_lable = QLabel('下载月份')
        else:
            month_lable = QLabel('Month')
        month_lable.setFont(font)
        month_lable.setAlignment(Qt.AlignRight)
        # month_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(month_lable, 2, 3)

        self.month_line = QLineEdit(self)
        self.month_line.setFont(font)
        if self.chinese:
            self.month_line.setPlaceholderText("无需填写")
        else:
            self.month_line.setPlaceholderText("Input not required.")
        self.month_line.setEnabled(False)
        # self.month_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.month_line, 2, 4, 1, 2)


        if self.chinese:
            begin_doy_lable = QLabel('起始日')
        else:
            begin_doy_lable = QLabel('Start Doy')
        begin_doy_lable.setFont(font)
        begin_doy_lable.setAlignment(Qt.AlignRight)
        # begin_doy_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(begin_doy_lable, 3, 0)

        self.begin_doy_line = QLineEdit(self)
        self.begin_doy_line.setFont(font)
        # self.begin_doy_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.begin_doy_line, 3, 1, 1, 2)

        if self.chinese:
            end_doy_lable = QLabel('截止日')
        else:
            end_doy_lable = QLabel('End Doy')
        end_doy_lable.setFont(font)
        end_doy_lable.setAlignment(Qt.AlignRight)
        # end_doy_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(end_doy_lable, 3, 3)

        self.end_doy_line = QLineEdit(self)
        self.end_doy_line.setFont(font)
        if self.chinese:
            self.end_doy_line.setPlaceholderText("仅下载单天数据时,无需填写此项")
        else:
            self.end_doy_line.setPlaceholderText("No fill for 1-day download.")
        # self.end_doy_line.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.end_doy_line, 3, 4, 1, 2)

        if self.chinese:
            pro_name_lable = QLabel('产品更名')
        else:
            pro_name_lable = QLabel('Rename')

        pro_name_lable.setFont(font)
        pro_name_lable.setAlignment(Qt.AlignRight)
        # site_name_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(pro_name_lable, 4, 0)

        self.pro_name_line = QLineEdit(self)
        self.pro_name_line.setFont(font)
        if self.chinese:
            self.pro_name_line.setPlaceholderText("若无更名需求,无需填写此项 [3char]")
        else:
            self.pro_name_line.setPlaceholderText("No fill if not needed. [3char]")
        # self.pro_name_line.setMinimumSize(QSize(lable_size, choose_h))
        type_choose_lay.addWidget(self.pro_name_line, 4, 1, 1, 2)

        if self.chinese:
            hour_lable = QLabel('小时选择')
        else:
            hour_lable = QLabel('Hour')
        hour_lable.setFont(font)
        hour_lable.setAlignment(Qt.AlignRight)
        # hour_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(hour_lable, 4, 3)

        self.hour_combo = QComboBox(self)
        for hour_combo_counter in range(0, 24):
            self.hour_combo.addItem(str(hour_combo_counter))
        self.hour_combo.addItem('0-23')
        self.hour_combo.setFont(font)
        self.hour_combo.setCurrentIndex(0)
        # self.hour_combo.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.hour_combo, 4, 4, 1, 2)

        if self.chinese:
            unzip_lable = QLabel('是否解压')
        else:
            unzip_lable = QLabel('Unzip')
        unzip_lable.setFont(font)
        unzip_lable.setAlignment(Qt.AlignRight)
        # unzip_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(unzip_lable, 5, 0)

        self.unzip_combo = QComboBox(self)
        if self.chinese:
            self.unzip_combo.addItem('是')
        else:
            self.unzip_combo.addItem('yes')
        if self.chinese:
            self.unzip_combo.addItem('否')
        else:
            self.unzip_combo.addItem('no')
        self.unzip_combo.setFont(font)
        # self.unzip_combo.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.unzip_combo, 5, 1, 1, 2)

        if self.chinese:
            pool_lable = QLabel('多线程数')
        else:
            pool_lable = QLabel('Thread')
        pool_lable.setFont(font)
        pool_lable.setAlignment(Qt.AlignRight)
        # pool_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(pool_lable, 5, 3)

        self.pool_combo = QComboBox(self)
        for pool_num_counter in range(1, 13):
            self.pool_combo.addItem(str(pool_num_counter))
        self.pool_combo.setFont(font)
        self.pool_combo.setCurrentIndex(4)
        # self.pool_combo.setMinimumSize(QSize(choose_size, choose_h))
        type_choose_lay.addWidget(self.pool_combo, 5, 4, 1, 2)

        if self.chinese:
            site_dir_lable = QLabel('站点列表')
        else:
            site_dir_lable = QLabel('Site')
        site_dir_lable.setFont(font)
        site_dir_lable.setAlignment(Qt.AlignRight)
        # site_dir_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(site_dir_lable, 6, 0)

        self.site_file_line = QLineEdit(self)
        self.site_file_line.setFont(font)
        if self.chinese:
            self.site_file_line.setPlaceholderText("按右侧按钮选择站点文件,或输入站点名称,按逗号分开 [bjfs,abpo]")
        else:
            self.site_file_line.setPlaceholderText("Select site files, or input site names separated by ',' [bjfs,abpo].")

        # self.site_file_line.setMinimumSize(QSize(int(screenWidth/3.2), choose_h))
        type_choose_lay.addWidget(self.site_file_line, 6, 1, 1, 4)

        open_site_file_btn = QPushButton('  ...  ', self)
        open_site_file_btn.setFont(font)
        open_site_file_btn.setMinimumSize(QSize(80, choose_h + 15))
        type_choose_lay.addWidget(open_site_file_btn, 6, 5, alignment=Qt.AlignRight)
        open_site_file_btn.clicked.connect(lambda: choose_site_file(self))

        if self.chinese:
            dd_dir_lable = QLabel('下载位置')
        else:
            dd_dir_lable = QLabel('Directory')
        dd_dir_lable.setFont(font)
        dd_dir_lable.setAlignment(Qt.AlignRight)
        # dd_dir_lable.setMinimumSize(QSize(lable_size, lable_h))
        type_choose_lay.addWidget(dd_dir_lable, 7, 0)

        self.out_dir_line = QLineEdit(self)
        self.out_dir_line.setFont(font)
        # self.out_dir_line.setMinimumSize(QSize(600, choose_h))
        if self.chinese:
            self.out_dir_line.setPlaceholderText("按右侧按钮选择下载文件夹,如不选择,则下载至程序所在路径")
        else:
            self.out_dir_line.setPlaceholderText("Select folder on right. If not, download to program path.")
        type_choose_lay.addWidget(self.out_dir_line, 7, 1, 1, 4)

        open_out_dir_btn = QPushButton('  ...  ', self)
        open_out_dir_btn.setFont(font)
        open_out_dir_btn.setMinimumSize(QSize(80, choose_h + 15))
        type_choose_lay.addWidget(open_out_dir_btn, 7, 5, alignment=Qt.AlignRight)
        open_out_dir_btn.clicked.connect(lambda: choose_out_dir(self))

        # none_lable = QLabel('')
        # type_choose_lay.addWidget(none_lable, 8, 0)

        font_big = QtGui.QFont()
        font_big.setPointSize(10)
        # font_big.setFamily('Microsoft YaHei')

        if self.chinese:
            dd_btn = QPushButton('下 载', self)
        else:
            dd_btn = QPushButton('DOWNLOAD', self)

        dd_btn.setFont(font_big)
        dd_btn.setMinimumSize(QSize(int(normalBtnSize*1.7), int(normalBtnH*1.2)))
        dd_btn.clicked.connect(lambda: dd(self))
        type_choose_lay.addWidget(dd_btn, 9, 1, 1, 2, alignment=Qt.AlignCenter)

        if self.chinese:
            kill_btn = QPushButton('终 止', self)
        else:
            kill_btn = QPushButton('STOP', self)
        kill_btn.setFont(font_big)
        kill_btn.setMinimumSize(QSize(int(normalBtnSize*1.7), int(normalBtnH*1.2)))
        kill_btn.clicked.connect(lambda: kill_p(self))
        type_choose_lay.addWidget(kill_btn, 9, 3, 1, 2, alignment=Qt.AlignCenter)

        RightTop = QFrame()
        RightTop.setFrameShape(QFrame.StyledPanel)
        RightTop.setLayout(type_choose_lay)

        # |--log打印控件 -> 右侧下方
        self.logPrint = QTextEdit()
        self.logPrint.document().setMaximumBlockCount(50)
        self.logPrint.setLineWrapMode(QTextEdit.NoWrap)
        self.logPrint.setTextInteractionFlags(Qt.TextSelectableByMouse)
        self.logPrint.setReadOnly(True)
        self.logPrint.setFont(font)

        printLog(self,'FAST Version : ' + lastVersion)
        printLog(self,'Compilation Date : ' + lastVersionTime)
        printLog(self,'Email : chuntaochang@whu.edu.cn')

        # 右侧控件布局设置
        splitterRight = QSplitter(Qt.Vertical)
        splitterRight.addWidget(RightTop)
        splitterRight.addWidget(self.logPrint)
        # splitterRight.setSizes([400, 200])
        # ----------------右侧控件布局----------------

        # ----------------总体控件布局----------------
        splitterAll = QSplitter(Qt.Horizontal)
        splitterAll.addWidget(splitterLeft)
        splitterAll.addWidget(splitterRight)
        splitterAll.setSizes([10, 80])
        # 声明布局
        downloadLayout = QHBoxLayout(self)
        downloadLayout.addWidget(splitterAll)

        #################### QC ####################
        qcMenu = QGridLayout()
        qcMenu.setSpacing(20)
        self.qcObsFile = None
        self.is_running = False  # 标记分析线程是否正在运行
        self.is_save_running = False  # 标记保存线程是否正在运行
        self.qcFreqData = None 
        self.qcSatNumData = None  
        self.qcCnrData = None  
        self.qcSlipData = None  
        self.qcHighData = None  
        self.qcMpData = None  
        self.qcCmcData = None  
        self.qcIodData = None  
        
        # 读取OBS文件
        self.qcObsFileChoose = QLineEdit(self)
        self.qcObsFileChoose.setFont(font)
        qcMenu.addWidget(self.qcObsFileChoose, 0, 0, 1, 1)

        self.qcChooseObsHead = None
        self.qcChooseObsData = None
        if self.chinese:
            self.qcChooseObsBtn = QPushButton('观测文件', self)
        else:
            self.qcChooseObsBtn = QPushButton('OBS', self)

        self.qcChooseObsBtn.setFont(font)
        self.qcChooseObsBtn.setMinimumSize(QSize(80, choose_h + 15))
        qcMenu.addWidget(self.qcChooseObsBtn, 0, 1,1,1, alignment=Qt.AlignRight)
        self.qcChooseObsBtn.clicked.connect(lambda: choose_obs_and_process(self))
        

        self.qcCombBox = QComboBox(self)
        if self.chinese:
            self.qcCombBox.addItem("频点序列")
            self.qcCombBox.addItem("卫星数量")
            self.qcCombBox.addItem("CNR")
            self.qcCombBox.addItem("周跳比")
            # self.qcCombBox.addItem("高次差")
            self.qcCombBox.addItem("相位噪声")
            self.qcCombBox.addItem("多路径")
            self.qcCombBox.addItem("CMC")
            self.qcCombBox.addItem("IOD")
        else:
            self.qcCombBox.addItem("Sat Vis")
            self.qcCombBox.addItem("Sat Num")
            self.qcCombBox.addItem("CNR")
            self.qcCombBox.addItem("CSR")
            # self.qcCombBox.addItem("HOD")
            self.qcCombBox.addItem("L_NOISE")
            self.qcCombBox.addItem("MP")
            self.qcCombBox.addItem("CMC")
            self.qcCombBox.addItem("IOD")
        
        self.qcCombBox.setFont(font)
        qcMenu.addWidget(self.qcCombBox, 1, 0, 1, 1)

        if self.chinese:
            qcChooseLable = QLabel('分析选择')
        else:
            qcChooseLable = QLabel('Options')
        qcChooseLable.setFont(font)
        qcChooseLable.setAlignment(Qt.AlignRight)
        # qcChooseLable.setMinimumSize(QSize(lable_size, lable_h))
        qcMenu.addWidget(qcChooseLable, 1, 1, 1, 1)
        
        # 
        self.qcChooseSysBox = ComboCheckBox([], None)
        self.qcChooseSysBox.setFont(font)
        qcMenu.addWidget(self.qcChooseSysBox, 2, 0, 1, 1)
        self.qcChooseSysBox.qLineEdit.textChanged.connect(lambda: qcSysChange(self))


        if self.chinese:
            qcChooseSysLable = QLabel('系统选择')
        else:
            qcChooseSysLable = QLabel('System')
        qcChooseSysLable.setFont(font)
        qcChooseSysLable.setAlignment(Qt.AlignRight)
        # qcChooseSysLable.setMinimumSize(QSize(lable_size, lable_h))
        qcMenu.addWidget(qcChooseSysLable, 2, 1, 1, 1)

        # PRN
        self.qcChoosePrnBox = ComboCheckBox([], None)
        self.qcChoosePrnBox.setFont(font)
        qcMenu.addWidget(self.qcChoosePrnBox, 3, 0, 1, 1)

        if self.chinese:
            qcChoosePrnLable = QLabel('卫星选择')
        else:
            qcChoosePrnLable = QLabel('PRN')
        qcChoosePrnLable.setFont(font)
        qcChoosePrnLable.setAlignment(Qt.AlignRight)
        # qcChoosePrnLable.setMinimumSize(QSize(lable_size, lable_h))
        qcMenu.addWidget(qcChoosePrnLable, 3, 1, 1, 1)


        self.qcChooseBandBox = ComboCheckBox([], None)
        self.qcChooseBandBox.setFont(font)
        qcMenu.addWidget(self.qcChooseBandBox, 4, 0, 1, 1)

        if self.chinese:
            qcChooseBandLable = QLabel('频点选择')
        else:
            qcChooseBandLable = QLabel('Freq')
        qcChooseBandLable.setFont(font)
        qcChooseBandLable.setAlignment(Qt.AlignRight)
        # qcChooseBandLable.setMinimumSize(QSize(lable_size, lable_h))
        qcMenu.addWidget(qcChooseBandLable, 4, 1, 1, 1)
        
        self.qcStartDateTimeEdit = QDateTimeEdit()
        self.qcStartDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
        self.qcStartDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
        self.qcStartDateTimeEdit.setFont(font)
        qcMenu.addWidget(self.qcStartDateTimeEdit, 5,0,1,1, alignment=Qt.AlignRight)
        
        if self.chinese:
            qcStartDateTimeLable = QLabel('开始时间')
        else:
            qcStartDateTimeLable = QLabel('Time Start')
        qcStartDateTimeLable.setFont(font)
        qcStartDateTimeLable.setAlignment(Qt.AlignRight)
        # qcStartDateTimeLable.setMinimumSize(QSize(lable_size, lable_h))
        qcMenu.addWidget(qcStartDateTimeLable, 5, 1, 1, 1)

        self.qcEndDateTimeEdit = QDateTimeEdit()
        self.qcEndDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
        self.qcEndDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
        self.qcEndDateTimeEdit.setFont(font)
        qcMenu.addWidget(self.qcEndDateTimeEdit, 6,0,1,1, alignment=Qt.AlignRight)

        if self.chinese:
            qcEndDateTimeLable = QLabel('结束时间')
        else:
            qcEndDateTimeLable = QLabel('Time End')
        qcEndDateTimeLable.setFont(font)
        qcEndDateTimeLable.setAlignment(Qt.AlignRight)
        qcMenu.addWidget(qcEndDateTimeLable, 6, 1, 1, 1)

        none_lable = QLabel('')
        qcMenu.addWidget(none_lable, 7, 0)

        if self.chinese:
            analyze_plot_btn = QPushButton('分析', self)
        else:
            analyze_plot_btn = QPushButton('PLOT', self)
        analyze_plot_btn.setFont(font)
        analyze_plot_btn.setMinimumSize(QSize(150, choose_h + 15))
        total_columns = qcMenu.columnCount()
        qcMenu.addWidget(analyze_plot_btn, 8,0,1, total_columns)
        analyze_plot_btn.clicked.connect(lambda: analyze_plot(self))

        if self.chinese:
            analyze_save_btn = QPushButton('保存', self)
        else:
            analyze_save_btn = QPushButton('SAVE', self)
        analyze_save_btn.setFont(font)
        analyze_save_btn.setMinimumSize(QSize(150, choose_h + 15))
        qcMenu.addWidget(analyze_save_btn, 9,0,1, total_columns)
        analyze_save_btn.clicked.connect(lambda: saveQcFile(self))
        
        if self.chinese:
            analyze_batch_btn = QPushButton('批量分析保存', self)
        else:
            analyze_batch_btn = QPushButton('Batch Analyze and Save', self)
        analyze_batch_btn.setFont(font)
        analyze_batch_btn.setMinimumSize(QSize(150, choose_h + 15))
        qcMenu.addWidget(analyze_batch_btn, 10,0,1, total_columns)
        analyze_batch_btn.clicked.connect(lambda: batch_analyze_plot(self))

        qcMenu.setColumnStretch(1, 1)

        qcLeft_in = QFrame()
        qcLeft_in.setFrameShape(QFrame.StyledPanel)
        qcLeft_in.setLayout(qcMenu)

        # 右侧tab
        self.qc_plot = QTabWidget()
        self.qc_plot.setTabPosition(QTabWidget.South)
        tabBar = self.qc_plot.tabBar()

        # 设置样式表
        tabBar.setStyleSheet("QTabBar::tab { min-width: " + str(int(screenWidth / 20)) + "%; min-height: " + str(int(screenHeight / 40)) + "%; }")

        # 频点序列图
        freqTab = QWidget()
        if self.chinese:
            self.qc_plot.addTab(freqTab, '频点序列')
        else:
            self.qc_plot.addTab(freqTab, 'Sat Vis')
        self.figFreq, self.axFreq = plt.subplots()
        # self.canvasFreq = self.figFreq.canvas
        self.canvasFreq = FigureCanvas(self.figFreq)
        freqTabLayout = QVBoxLayout(freqTab)
        freqTabLayout.addWidget(self.canvasFreq)

        # 卫星数量
        satnumTab = QWidget()
        if self.chinese:
            self.qc_plot.addTab(satnumTab, '卫星数量')
        else:
            self.qc_plot.addTab(satnumTab, 'Sat Num')

        self.figsatnum, self.axsatnum = plt.subplots()
        self.canvassatnum = self.figsatnum.canvas
        satnumTabLayout = QVBoxLayout(satnumTab)
        satnumTabLayout.addWidget(self.canvassatnum)

        # 载噪比
        cnrTab = QWidget()
        self.qc_plot.addTab(cnrTab, 'CNR')
        self.figcnr, self.axcnr = plt.subplots()
        self.canvascnr = self.figcnr.canvas
        cnrTabLayout = QVBoxLayout(cnrTab)
        cnrTabLayout.addWidget(self.canvascnr)

        # SLIP
        cycleSlipTab = QWidget()
        if self.chinese:
            self.qc_plot.addTab(cycleSlipTab, '周跳比')
        else:
            self.qc_plot.addTab(cycleSlipTab, 'CSR')
        self.figCycleSlip, self.axCycleSlip = plt.subplots(figsize=(6, 5))
        self.canvascycleSlip = self.figCycleSlip.canvas
        cycleSlipTabLayout = QVBoxLayout(cycleSlipTab)
        cycleSlipTabLayout.addWidget(self.canvascycleSlip)

        # 相位噪声
        phaseNoiseTab = QWidget()
        if self.chinese:
            self.qc_plot.addTab(phaseNoiseTab, '相位噪声')
        else:
            self.qc_plot.addTab(phaseNoiseTab, 'L_NOISE')
        self.figPhaseNoise, self.axPhaseNoise = plt.subplots()
        self.canvasPhaseNoise = self.figPhaseNoise.canvas
        phaseNoiseTabLayout = QVBoxLayout(phaseNoiseTab)
        phaseNoiseTabLayout.addWidget(self.canvasPhaseNoise)

        # 多路径
        MPTab = QWidget()
        if self.chinese:
            self.qc_plot.addTab(MPTab, '多路径')
        else:
            self.qc_plot.addTab(MPTab, 'MP')
        self.figMP, self.axMP = plt.subplots()
        self.canvasMP = self.figMP.canvas
        MPTabLayout = QVBoxLayout(MPTab)
        MPTabLayout.addWidget(self.canvasMP)

        # CMC
        CMCTab = QWidget()
        self.qc_plot.addTab(CMCTab, 'CMC')
        self.figCMC, self.axCMC = plt.subplots()
        self.canvasCMC = self.figCMC.canvas
        CMCTabLayout = QVBoxLayout(CMCTab)
        CMCTabLayout.addWidget(self.canvasCMC)

        # 电离层延迟变化
        iodTab = QWidget()
        self.qc_plot.addTab(iodTab, 'IOD')
        self.figIOD, self.axIOD = plt.subplots()
        self.canvasIOD = self.figIOD.canvas
        iodTabLayout = QVBoxLayout(iodTab)
        iodTabLayout.addWidget(self.canvasIOD)

        self.qc_plot.setStyleSheet("""
            QTabBar::tab {
                min-height: 10px;    /* 更激进的高度 */
                max-height: 10px;
                padding: 0px 4px;
                font-size: 18px;
                margin: 1;
            }
        """)

        qcRight_in = QFrame()
        qcRight_in.setFrameShape(QFrame.StyledPanel)

        qcRight_in.setLayout(QHBoxLayout())
        qcRight_in.layout().addWidget(self.qc_plot)

        # QC左侧控件布局
        qcLeft = QSplitter(Qt.Vertical)
        qcLeft.addWidget(qcLeft_in)

        # QC右侧控件布局
        qcRight = QSplitter(Qt.Vertical)
        qcRight.addWidget(qcRight_in)

        qcAllLayout = QSplitter(Qt.Horizontal)
        qcAllLayout.addWidget(qcLeft)
        qcAllLayout.addWidget(qcRight)
        qcAllLayout.setStretchFactor(1, 3)

        qcLayout = QHBoxLayout(self)
        qcLayout.addWidget(qcAllLayout)
        #################### QC ####################

        #################### SPP ###################
        sppMenu = QGridLayout()
        sppMenu.setSpacing(20)
        self.isSppRunning = False  # 标记线程是否正在运行
        self.isSppSaving = False
        self.posData = None

        # 读取OBS文件
        self.sppObsFileChoose = QLineEdit(self)
        self.sppObsFileChoose.setFont(font)
        sppMenu.addWidget(self.sppObsFileChoose, 0, 0, 1, 1)

        self.sppChooseObsHead = None
        self.sppChooseObsData = None
        self.sppSysBand = []
        if self.chinese:
            self.sppChooseObsBtn = QPushButton('观测文件', self)
        else:
            self.sppChooseObsBtn = QPushButton('OBS', self)
        self.sppChooseObsBtn.setFont(font)
        self.sppChooseObsBtn.setMinimumSize(QSize(80, choose_h + 15))
        sppMenu.addWidget(self.sppChooseObsBtn, 0, 1,1,1, alignment=Qt.AlignRight)
        self.sppChooseObsBtn.clicked.connect(lambda: sppChooseObsProcess(self))

        # 读取NAV文件
        self.sppNavFileChoose = QLineEdit(self)
        self.sppNavFileChoose.setFont(font)
        sppMenu.addWidget(self.sppNavFileChoose, 1, 0, 1, 1)

        self.sppChooseNavData = None
        if self.chinese:
            self.sppChooseNavBtn = QPushButton('广播星历', self)
        else:
            self.sppChooseNavBtn = QPushButton('NAV', self)
        self.sppChooseNavBtn.setFont(font)
        self.sppChooseNavBtn.setMinimumSize(QSize(80, choose_h + 15))
        sppMenu.addWidget(self.sppChooseNavBtn, 1, 1,1,1, alignment=Qt.AlignRight)
        self.sppChooseNavBtn.clicked.connect(lambda: sppChooseNav(self))


        self.sppStartDateTimeEdit = QDateTimeEdit()
        self.sppStartDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
        self.sppStartDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
        self.sppStartDateTimeEdit.setFont(font)
        sppMenu.addWidget(self.sppStartDateTimeEdit, 3,0,1,1, alignment=Qt.AlignRight)
        if self.chinese:
            sppStartDateTimeLable = QLabel('开始时间')
        else:
            sppStartDateTimeLable = QLabel('Time Start')
        sppStartDateTimeLable.setFont(font)
        sppStartDateTimeLable.setAlignment(Qt.AlignRight)
        # sppStartDateTimeLable.setMinimumSize(QSize(lable_size, lable_h))
        sppMenu.addWidget(sppStartDateTimeLable, 3, 1, 1, 1)

        self.sppEndDateTimeEdit = QDateTimeEdit()
        self.sppEndDateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
        self.sppEndDateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
        self.sppEndDateTimeEdit.setFont(font)
        sppMenu.addWidget(self.sppEndDateTimeEdit, 4,0,1,1, alignment=Qt.AlignRight)

        if self.chinese:
            sppEndDateTimeLable = QLabel('结束时间')
        else:
            sppEndDateTimeLable = QLabel('Time End')
        sppEndDateTimeLable.setFont(font)
        sppEndDateTimeLable.setAlignment(Qt.AlignRight)
        # sppEndDateTimeLable.setMinimumSize(QSize(lable_size, lable_h))
        sppMenu.addWidget(sppEndDateTimeLable, 4, 1, 1, 1)

        self.sppChooseSysCombBox = ComboCheckBox(['GPS', 'GAL', 'BDS'], None)
        sppMenu.addWidget(self.sppChooseSysCombBox, 5, 0, 1, 1)
        sppSYSLable = QLabel('System')
        sppSYSLable.setFont(font)
        sppSYSLable.setAlignment(Qt.AlignRight)
        # sppSYSLable.setMinimumSize(QSize(lable_size, lable_h))
        sppMenu.addWidget(sppSYSLable, 5, 1, 1, 1)

        none_lable = QLabel('')
        sppMenu.addWidget(none_lable, 11, 0)

        if self.chinese:
            runSppBtn = QPushButton('运行', self)
        else:
            runSppBtn = QPushButton('Run', self)
        runSppBtn.setFont(font)
        runSppBtn.setMinimumSize(QSize(150, choose_h + 15))
        total_columns = sppMenu.columnCount()
        sppMenu.addWidget(runSppBtn, 12,0,1, total_columns)
        runSppBtn.clicked.connect(lambda: runSpp(self))

        if self.chinese:
            saveSppBtn = QPushButton('保存', self)
        else:
            saveSppBtn = QPushButton('SAVE', self)
        saveSppBtn.setFont(font)
        saveSppBtn.setMinimumSize(QSize(150, choose_h + 15))
        sppMenu.addWidget(saveSppBtn, 13,0,1, total_columns)
        saveSppBtn.clicked.connect(lambda: saveSppPos(self))

        sppLeft_in = QFrame()
        sppLeft_in.setFrameShape(QFrame.StyledPanel)
        sppMenu.setColumnStretch(1, 1)
        sppLeft_in.setLayout(sppMenu)

        sppRight_in = QFrame()
        sppRight_in.setFrameShape(QFrame.StyledPanel)

        self.figSPP, self.axSPP = plt.subplots()
        self.canvasSPP = self.figSPP.canvas

        sppRight_in.setLayout(QHBoxLayout())
        sppRight_in.layout().addWidget(self.canvasSPP)

        # SPP左侧控件布局
        sppLeft = QSplitter(Qt.Vertical)
        sppLeft.addWidget(sppLeft_in)

        # SPP右侧控件布局
        sppRight = QSplitter(Qt.Vertical)
        sppRight.addWidget(sppRight_in)

        sppAllLayout = QSplitter(Qt.Horizontal)
        sppAllLayout.addWidget(sppLeft)
        sppAllLayout.addWidget(sppRight)
        sppAllLayout.setStretchFactor(1, 3)

        sppLayout = QHBoxLayout(self)
        sppLayout.addWidget(sppAllLayout)

        #################### SPP ###################


        ################### SITE ###################
        siteMenu = QGridLayout()
        siteMenu.setSpacing(20)
        self.isSiteRunning = False  # 标记线程是否正在运行
        self.chooseSite = {}

        # 上方地图
        siteTop_in = QFrame()
        siteTop_in.setFrameShape(QFrame.StyledPanel)

        # 绘图初始化
        mpl.rcParams['axes.unicode_minus'] = False
        mpl.rc('xtick', labelsize=15)
        mpl.rc('ytick', labelsize=15)
        mpl.rcParams['xtick.direction'] = 'in'
        mpl.rcParams['ytick.direction'] = 'in'
        self.figsite = plt.figure()
        self.figsite.clf()
        self.axsite = self.figsite.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())
        self.axsite.set_global()
        self.axsite.add_feature(cfeature.LAND, facecolor='antiquewhite',zorder=20)
        self.axsite.add_feature(cfeature.OCEAN, facecolor='steelblue',zorder=0)
        self.gl = self.axsite.gridlines(color='white', alpha=0.2, draw_labels=True, dms=True, x_inline=False, y_inline=False,zorder=10)
        self.axsite.set_extent([-180, 180, -90, 90], crs=ccrs.PlateCarree())
        self.figsite.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95)
        self.canvassite = self.figsite.canvas

        siteTop_in.setLayout(QHBoxLayout())
        siteTop_in.layout().addWidget(self.canvassite)

        # 下方选项
        siteDown_in = QFrame()
        siteDown_in.setFrameShape(QFrame.StyledPanel)
        siteDown_in.setLayout(siteMenu)

        self.siteCombBox = QComboBox(self)
        self.siteCombBox.addItem("ALL IGS  SITE")
        self.siteCombBox.addItem("IGS LIST FILE - e.g(bjfs irkj urum)")
        self.siteCombBox.addItem("SITE FILE     - e.g(L, B, siteName)")
        self.siteCombBox.setMinimumSize(QSize(70, lable_h))
        self.siteCombBox.currentIndexChanged.connect(lambda: siteCombBoxChanged(self))
        siteMenu.addWidget(self.siteCombBox, 0, 0, 1, 2)

        # 读取站点文件
        self.siteFileChoose = QLineEdit(self)
        self.siteFileChoose.setFont(font)
        # self.siteFileChoose.setMinimumSize(QSize(40, lable_h))
        siteMenu.addWidget(self.siteFileChoose, 1, 0, 1, 1)
        self.siteFileChoose.setEnabled(False)

        self.siteFileData = None
        self.siteChooseFileBtn = QPushButton('Select File', self)
        self.siteChooseFileBtn.setFont(font)
        # self.siteChooseFileBtn.setMinimumSize(QSize(40, choose_h + 15))
        siteMenu.addWidget(self.siteChooseFileBtn, 1,1,1,1, alignment=Qt.AlignRight)
        self.siteChooseFileBtn.clicked.connect(lambda: siteChooseFileProcess(self))
        self.siteChooseFileBtn.setEnabled(False)

        # 
        self.igsSiteSys = ComboCheckBox(['GPS', 'GLO', 'GAL', 'BDS', 'SBAS', 'QZSS', 'IRNSS'], None)
        self.igsSiteSys.setMinimumSize(QSize(40, lable_h))
        self.igsSiteSys.qCheckBox[0].setChecked(True)
        siteMenu.addWidget(self.igsSiteSys, 2, 0, 1, 1)

        igsSiteSysLable = QLabel('GNSS System')
        igsSiteSysLable.setFont(font)
        igsSiteSysLable.setAlignment(Qt.AlignRight)
        # igsSiteSysLable.setMinimumSize(QSize(40, lable_h))
        siteMenu.addWidget(igsSiteSysLable, 2, 1, 1, 1)

        # 
        self.igsAntList = ['TRM57971.00', 'ASH701945G_M', 'TRM59800.99', 'TRM159800.00', 
                                         'SEPCHOKE_B3E6', 'TRM59800.80', 'LEIAR20', 'LEIAR25.R4', 'TRM59800.00', 
                                         'TRM115000.00', 'AOAD/M_T', 'LEIAR25.R3', 'ASH701945D_M', 'TPSCR.G5C', 
                                         'JAVRINGANT_DM', 'ASH700936D_M', 'STXSA1500', 'ASH701945C_M', 'TRM55971.00', 
                                         'TPSCR.G3', 'LEIAR10', 'TPSCR.G5', 'JAV_RINGANT_G3T', 'TRM59900.00', 'NOV702GG', 
                                         'TWIVC6150', 'LEIAT504', 'ASH701945B_M', 'ASH701945E_M', 'JAV_GRANT-G3T', 
                                         'ASH701941.B', 'TWIVC6050', 'JAVRINGANT_G5T', 'NOV750.R4', 'TRM159900.00', 
                                         'LEIAT504GG', 'LEIAX1202GG', 'SEPCHOKE_MC', 'JPSREGANT_SD_E1', 'JNSCR_C146-22-1', 
                                         'TPSCR3_GGD', 'AOAD/M_T_RFI_T', 'ASH700936A_M', 'CHCC220GR2', 'LEIAR25', 
                                         'JPSREGANT_DD_E1', 'ASH700936C_M', 'ASH701073.1', 'AOAD/M_B', '3S-02-TSADM', 
                                         'ASH701933B_M', 'TRM29659.00', 'TRM41249.00', 'HITAT45101CP', 'HXCCGX601A', 'TRM59800.00C']
        self.igsAntList.sort()
        self.igsAntListComboCheck = ComboCheckBox(self.igsAntList, None)
        # self.igsAntListComboCheck.setMinimumSize(QSize(40, lable_h))
        for i in range(self.igsAntListComboCheck.row_num):
            self.igsAntListComboCheck.qCheckBox[i].setChecked(True)
        siteMenu.addWidget(self.igsAntListComboCheck, 3, 0, 1, 1)

        antLable = QLabel('AntennaName')
        antLable.setFont(font)
        antLable.setAlignment(Qt.AlignRight)
        # antLable.setMinimumSize(QSize(40, lable_h))
        siteMenu.addWidget(antLable, 3, 1, 1, 1)

        
        none_lable0 = QLabel('')
        none_lable0.setMinimumSize(QSize(60, normalBtnH))
        siteMenu.addWidget(none_lable0, 0, 2, 4, 1)

        stationSelLable = QLabel('Station Selection')
        stationSelLable.setFont(font)
        stationSelLable.setAlignment(Qt.AlignCenter)
        # stationSelLable.setMinimumSize(QSize(70, lable_h))
        siteMenu.addWidget(stationSelLable, 0, 3, 1, 3)


        self.thinningLine = QLineEdit(self)
        self.thinningLine.setFont(font)
        # self.thinningLine.setMinimumSize(QSize(400, lable_h))
        siteMenu.addWidget(self.thinningLine, 1, 3, 1, 2)

        thinningLable = QLabel('Thinning  [deg]')
        thinningLable.setFont(font)
        thinningLable.setAlignment(Qt.AlignRight)
        # thinningLable.setMinimumSize(QSize(140, lable_h))
        siteMenu.addWidget(thinningLable, 1, 5, 1, 1)


        self.LminLine = QLineEdit(self)
        self.LminLine.setFont(font)
        # self.LminLine.setMinimumSize(QSize(140, lable_h))
        self.LminLine.setText('-180')
        siteMenu.addWidget(self.LminLine, 2, 3, 1, 1)

        self.LmaxLine = QLineEdit(self)
        self.LmaxLine.setFont(font)
        self.LmaxLine.setText('180')
        # self.LmaxLine.setMinimumSize(QSize(140, lable_h))
        siteMenu.addWidget(self.LmaxLine, 2, 4, 1, 1)

        LRangeLable = QLabel('L  Range  [deg]')
        LRangeLable.setFont(font)
        # LRangeLable.setAlignment(Qt.AlignRight)
        # LRangeLable.setMinimumSize(QSize(40, lable_h))
        siteMenu.addWidget(LRangeLable, 2, 5, 1, 1)


        self.BminLine = QLineEdit(self)
        self.BminLine.setFont(font)
        self.BminLine.setText('-90')
        # self.BminLine.setMinimumSize(QSize(140, lable_h))
        siteMenu.addWidget(self.BminLine, 3, 3, 1, 1)

        self.BmaxLine = QLineEdit(self)
        self.BmaxLine.setFont(font)
        self.BmaxLine.setText('90')
        # self.BmaxLine.setMinimumSize(QSize(140, lable_h))
        siteMenu.addWidget(self.BmaxLine, 3, 4, 1, 1)

        BRangeLable = QLabel('B  Range  [deg]')
        BRangeLable.setFont(font)
        # BRangeLable.setAlignment(Qt.AlignRight)
        # BRangeLable.setMinimumSize(QSize(40, lable_h))
        siteMenu.addWidget(BRangeLable, 3, 5, 1, 1)

        none_lable = QLabel('')
        none_lable.setMinimumSize(QSize(60, normalBtnH))
        siteMenu.addWidget(none_lable, 0, 6, 4, 1)

        self.siteNameCheckBox = QCheckBox('SITE NAME')
        self.siteNameCheckBox.setFont(font)
        self.siteNameCheckBox.setMinimumSize(QSize(200, normalBtnH))
        siteMenu.addWidget(self.siteNameCheckBox, 0,7,1,1)
        

        self.globalCheckBox = QCheckBox('SET GLOBAL', self)
        self.globalCheckBox.setFont(font)
        # self.globalCheckBox.setMinimumSize(QSize(80, normalBtnH))
        siteMenu.addWidget(self.globalCheckBox, 1,7,1,1)
        self.globalCheckBox.setChecked(True)

        self.siteRefreshBtn = QPushButton('PLOT', self)
        self.siteRefreshBtn.setFont(font)
        self.siteRefreshBtn.setMinimumSize(QSize(125, normalBtnH))
        siteMenu.addWidget(self.siteRefreshBtn, 2,7,1,1)
        self.siteRefreshBtn.clicked.connect(lambda: sitePlotProcess(self))
        

        self.siteSaveFileBtn = QPushButton('SAVE', self)
        self.siteSaveFileBtn.setFont(font)
        self.siteSaveFileBtn.setMinimumSize(QSize(125, normalBtnH))
        self.siteSaveFileBtn.clicked.connect(lambda: saveSite(self))
        siteMenu.addWidget(self.siteSaveFileBtn, 3,7,1,1)

        none_lable2 = QLabel('')
        none_lable2.setMinimumSize(QSize(60, normalBtnH))
        siteMenu.addWidget(none_lable2, 0, 8, 4, 1)

        # site上侧控件布局
        siteTop = QSplitter(Qt.Vertical)
        siteTop.addWidget(siteTop_in)

        # site下侧控件布局
        siteDown = QSplitter(Qt.Vertical)
        siteDown.addWidget(siteDown_in)

        # siteAllLayout = QSplitter(Qt.Horizontal)
        siteAllLayout = QSplitter(Qt.Vertical)
        siteAllLayout.addWidget(siteTop)
        siteAllLayout.addWidget(siteDown)
        siteAllLayout.setStretchFactor(3, 1)

        siteLayout = QHBoxLayout(self)
        siteLayout.addWidget(siteAllLayout)

        ################### SITE ###################


        main_widget = QWidget(self)
        main_layout = QVBoxLayout(main_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)

        # 创建 QTabWidget
        tab_widget = QTabWidget()
                
        # 将选项卡放在左侧 
        # tab_widget.setStyleSheet("QTabBar::tab { min-width: " + str(int(screenWidth / 13)) + "%; min-height: " + str(int(screenHeight / 40)) + "%; }")  # 设置tab_widget的宽度为100%
        # tab_widget.setTabPosition(QTabWidget.North)

        # 声明QWidget
        downloadFrame = QWidget()
        downloadFrame.setFont(font)
        downloadFrame.setLayout(downloadLayout)
        self.setCentralWidget(downloadFrame)
        if self.chinese:
            tab_widget.addTab(downloadFrame, "数据下载")
        else:
            tab_widget.addTab(downloadFrame, "Download")

        qcFrame = QWidget()
        qcFrame.setFont(font)
        qcFrame.setLayout(qcLayout)
        if self.chinese:
            tab_widget.addTab(qcFrame, "数据分析")
        else:
            tab_widget.addTab(qcFrame, "Analyze")


        sppFrame = QWidget()
        sppFrame.setFont(font)
        sppFrame.setLayout(sppLayout)
        if self.chinese:
            tab_widget.addTab(sppFrame, "单点定位")
        else:
            tab_widget.addTab(sppFrame, 'SPP')
    

        siteFrame = QWidget()
        siteFrame.setFont(font)
        siteFrame.setLayout(siteLayout)
        if self.chinese:
            tab_widget.addTab(siteFrame, "选站绘图")
        else:
            tab_widget.addTab(siteFrame, 'Site select')

        # toolFrame = QWidget()
        # tab_widget.addTab(toolFrame, "其他工具")


        # tab_widget.setStyleSheet("""
        #     QTabBar::tab {
        #         border: none;
        #     }
        # """)
        tab_widget.setStyleSheet("""
            QTabBar::tab {
                margin: 1;       /* 移除外边距 */
                padding: 10px 60px; /* 减少内边距 */
            }
        """)
        # 将 QTabWidget 添加到主窗口布局
        main_layout.addWidget(tab_widget, stretch=1)

        # 设置主窗口部件为中央部件
        self.setCentralWidget(main_widget)

        # 展示
        self.show()
        # ----------------总体控件布局----------------

def fastAppMain():

    fastApp = QApplication(sys.argv)
    whuLoadPng = os.path.join(dirname, 'win_bin', 'black_2_1.png')
    splash_pix = QPixmap(whuLoadPng)  
    target_size = QSize(800, 400)  
    splash_pix = splash_pix.scaled(target_size, Qt.AspectRatioMode.KeepAspectRatio)
    splash = QSplashScreen(splash_pix, Qt.WindowStaysOnTopHint)
    splash.show()
    fastApp.setStyleSheet(qdarkstyle.load_stylesheet())

    
    framelessWnd = FramelessWindow()
    whu_ico = os.path.join(dirname, 'win_bin', 'black_c.ico')
    framelessWnd.setWindowIcon(QtGui.QIcon(whu_ico))
    framelessWnd.setWindowTitle('FAST V' + lastVersion)
    
    # framelessWnd.setWindowOpacity(0.98)
    # framelessWnd.resize(300, 300)
    ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID("myappid")

    settingFile = os.path.join(dirname, 'win_bin', 'setting')
    fastQtSetting = getSetting(settingFile)
    win = mainWindow(fastQtSetting)
    framelessWnd.setContent(win)
    splash.close()
    framelessWnd.show()
    sys.exit(fastApp.exec())


if __name__ == '__main__':
    fastAppMain()
