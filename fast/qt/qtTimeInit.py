# -*- coding: utf-8 -*-
# FAST           : Time UI Initialization
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2026.03.18

from PyQt5.QtWidgets import QHBoxLayout, QFrame, QWidget, QSplitter, QLabel, \
    QPushButton, QLineEdit, QVBoxLayout
from PyQt5.QtCore import Qt, QSize
from fast.qt.timeTran import time_tran, time_tran_none


def init_time_ui(main_win, font, chinese, normalBtnSize, normalBtnH):
    """初始化时间转换模块UI"""
    # GPS Datetime标签
    datetime_Label_box = QHBoxLayout()
    datetime_Label = QLabel("GPS Datetime")
    datetime_Label.setFont(font)
    datetime_Label.setAlignment(Qt.AlignCenter)
    datetime_Label_box.addWidget(datetime_Label)
    datetime_Label_wg = QWidget()
    datetime_Label_wg.setLayout(datetime_Label_box)

    # 日期时间选择器
    from PyQt5.QtWidgets import QDateTimeEdit
    from PyQt5.QtCore import QDateTime
    dateTimeEdit_box = QHBoxLayout()
    main_win.dateTimeEdit = QDateTimeEdit()
    main_win.dateTimeEdit.setDisplayFormat("yyyy-MM-dd  h:m:ss")
    main_win.dateTimeEdit.setDateTime(QDateTime.currentDateTimeUtc())
    main_win.dateTimeEdit.setFont(font)
    dateTimeEdit_box.addWidget(main_win.dateTimeEdit)
    dateTimeEdit_wg = QWidget()
    dateTimeEdit_wg.setLayout(dateTimeEdit_box)

    # Year/Month/Day标签
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

    # Year/Month/Day输入框
    ymd_box = QHBoxLayout()
    main_win.year_text = QLineEdit(main_win)
    main_win.year_text.setFont(font)
    main_win.year_text.setAlignment(Qt.AlignCenter)
    main_win.month_text = QLineEdit(main_win)
    main_win.month_text.setFont(font)
    main_win.month_text.setAlignment(Qt.AlignCenter)
    main_win.day_text = QLineEdit(main_win)
    main_win.day_text.setAlignment(Qt.AlignCenter)
    main_win.day_text.setFont(font)
    ymd_box.addWidget(main_win.year_text)
    ymd_box.addWidget(main_win.month_text)
    ymd_box.addWidget(main_win.day_text)
    ymd_wg = QWidget()
    ymd_wg.setLayout(ymd_box)

    # Year/Doy标签
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

    # Year/Doy输入框
    ydoy_box = QHBoxLayout()
    main_win.yearofdoy_text = QLineEdit(main_win)
    main_win.yearofdoy_text.setFont(font)
    main_win.yearofdoy_text.setAlignment(Qt.AlignCenter)
    main_win.doy_text = QLineEdit(main_win)
    main_win.doy_text.setFont(font)
    main_win.doy_text.setAlignment(Qt.AlignCenter)
    ydoy_box.addWidget(main_win.yearofdoy_text)
    ydoy_box.addWidget(main_win.doy_text)
    ydoy_wg = QWidget()
    ydoy_wg.setLayout(ydoy_box)

    # GPS Week标签
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

    # GPS Week输入框
    gpsweekd_box = QHBoxLayout()
    main_win.gpsweek_text = QLineEdit(main_win)
    main_win.gpsweek_text.setFont(font)
    main_win.gpsweek_text.setAlignment(Qt.AlignCenter)
    main_win.gpsdow_text = QLineEdit(main_win)
    main_win.gpsdow_text.setFont(font)
    main_win.gpsdow_text.setAlignment(Qt.AlignCenter)
    gpsweekd_box.addWidget(main_win.gpsweek_text)
    gpsweekd_box.addWidget(main_win.gpsdow_text)
    gpsweekd_wg = QWidget()
    gpsweekd_wg.setLayout(gpsweekd_box)

    # BDS Week标签
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

    # BDS Week输入框
    bdsweekd_box = QHBoxLayout()
    main_win.bdsweek_text = QLineEdit(main_win)
    main_win.bdsweek_text.setFont(font)
    main_win.bdsweek_text.setAlignment(Qt.AlignCenter)
    main_win.bdsdow_text = QLineEdit(main_win)
    main_win.bdsdow_text.setFont(font)
    main_win.bdsdow_text.setAlignment(Qt.AlignCenter)
    bdsweekd_box.addWidget(main_win.bdsweek_text)
    bdsweekd_box.addWidget(main_win.bdsdow_text)
    bdsweekd_wg = QWidget()
    bdsweekd_wg.setLayout(bdsweekd_box)

    # MJD/SOD标签
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

    # 空标签
    none_Label_box = QHBoxLayout()
    none_Label = QLabel("")
    none_Label_box.addWidget(none_Label)
    none_Label_wg = QWidget()
    none_Label_wg.setLayout(none_Label_box)

    # MJD/SOD输入框
    mjdsod_box = QHBoxLayout()
    main_win.mjd_text = QLineEdit(main_win)
    main_win.mjd_text.setAlignment(Qt.AlignCenter)
    main_win.mjd_text.setFont(font)
    main_win.sod_text = QLineEdit(main_win)
    main_win.sod_text.setAlignment(Qt.AlignCenter)
    main_win.sod_text.setFont(font)
    mjdsod_box.addWidget(main_win.mjd_text)
    mjdsod_box.addWidget(main_win.sod_text)
    mjdsod_wg = QWidget()
    mjdsod_wg.setLayout(mjdsod_box)

    # 转换/清空按钮
    time_tran_box = QHBoxLayout()
    if chinese:
        time_tran_btn = QPushButton('转换', main_win)
    else:
        time_tran_btn = QPushButton('TRANS', main_win)
    time_tran_btn.setFont(font)
    time_tran_btn.setMinimumSize(QSize(normalBtnSize, normalBtnH))
    time_tran_btn.clicked.connect(lambda: time_tran(main_win))

    if chinese:
        time_tran_none_btn = QPushButton('清空', main_win)
    else:
        time_tran_none_btn = QPushButton('CLEAR', main_win)
    time_tran_none_btn.setFont(font)
    time_tran_none_btn.setMinimumSize(QSize(normalBtnSize, normalBtnH))
    time_tran_none_btn.clicked.connect(lambda: time_tran_none(main_win))

    time_tran_box.addWidget(time_tran_btn)
    time_tran_box.addWidget(time_tran_none_btn)
    time_tran_wg = QWidget()
    time_tran_wg.setLayout(time_tran_box)

    # 组装时间布局
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

    splitterLeft = QSplitter(Qt.Vertical)
    splitterLeft.addWidget(splitterLeft_in)
    
    return splitterLeft
