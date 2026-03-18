# -*- coding: utf-8 -*-
# FAST           : Qt UI Initialization Entry Point
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2026.03.17

from PyQt5.QtWidgets import QTabWidget, QWidget, QVBoxLayout
from fast.qt.qtStyle import get_tab_style

# 导入各模块UI初始化函数
from fast.qt.qtTimeInit import init_time_ui
from fast.qt.qtDownloadInit import init_download_ui
from fast.qt.qtQcInit import init_qc_ui
from fast.qt.qtSppInit import init_spp_ui
from fast.qt.qtSiteInit import init_site_ui


def init_main_tabs(main_win, font, chinese, downloadLayout, qcLayout, sppLayout, siteLayout):
    """初始化主Tab布局"""
    main_widget = QWidget(main_win)
    main_layout = QVBoxLayout(main_widget)
    main_layout.setContentsMargins(0, 0, 0, 0)

    tab_widget = QTabWidget()

    # Download Tab
    downloadFrame = QWidget()
    downloadFrame.setFont(font)
    downloadFrame.setLayout(downloadLayout)
    main_win.setCentralWidget(downloadFrame)
    if chinese:
        tab_widget.addTab(downloadFrame, "数据下载")
    else:
        tab_widget.addTab(downloadFrame, "Download")

    # QC Tab
    qcFrame = QWidget()
    qcFrame.setFont(font)
    qcFrame.setLayout(qcLayout)
    if chinese:
        tab_widget.addTab(qcFrame, "数据分析")
    else:
        tab_widget.addTab(qcFrame, "Analyze")

    # SPP Tab
    sppFrame = QWidget()
    sppFrame.setFont(font)
    sppFrame.setLayout(sppLayout)
    if chinese:
        tab_widget.addTab(sppFrame, "单点定位")
    else:
        tab_widget.addTab(sppFrame, 'SPP')

    # Site Tab
    siteFrame = QWidget()
    siteFrame.setFont(font)
    siteFrame.setLayout(siteLayout)
    if chinese:
        tab_widget.addTab(siteFrame, "选站绘图")
    else:
        tab_widget.addTab(siteFrame, 'Site select')

    tab_widget.setStyleSheet(get_tab_style())

    main_layout.addWidget(tab_widget, stretch=1)
    main_win.setCentralWidget(main_widget)
    main_win.show()