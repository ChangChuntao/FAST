# -*- coding: utf-8 -*-
# FAST           : Download UI Initialization
# Author         : Chang Chuntao
# Copyright(C)   : The GNSS Center, Wuhan University
# Creation       : 2026.03.18

from PyQt5.QtWidgets import QGridLayout, QComboBox, QTextEdit, QFrame, \
    QSplitter, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import Qt, QSize
from fast.com.pub import gnss_type
from fast.qt.qtStyle import (
    get_small_btn_style, get_primary_btn_style, 
    get_danger_btn_style, get_log_style, apply_download_styles
)
from fast.qt.qtDownload import (
    choose_site_file, choose_out_dir, dd, kill_p, 
    printLog, dataTypeOnActivated, nameTypeOnActivated
)


def init_download_ui(main_win, font, font_big, chinese, lable_size, lable_h, 
                     choose_size, choose_h, normalBtnSize, normalBtnH, lastVersion, lastVersionTime):
    """初始化下载模块UI"""
    
    # 内部辅助函数：创建Label
    def create_label(text_cn, text_en, row, col, alignment=Qt.AlignRight):
        label = QLabel(text_cn if chinese else text_en)
        label.setFont(font)
        label.setAlignment(alignment)
        layout.addWidget(label, row, col)
        return label

    # 内部辅助函数：创建ComboBox
    def create_combo(items, row, col, colspan=2, current_index=0):
        combo = QComboBox(main_win)
        combo.addItems(items)
        combo.setFont(font)
        combo.setCurrentIndex(current_index)
        layout.addWidget(combo, row, col, 1, colspan)
        return combo

    # 内部辅助函数：创建LineEdit
    def create_line_edit(placeholder_cn=None, placeholder_en=None, enabled=True, row=None, col=None, colspan=2):
        line = QLineEdit(main_win)
        line.setFont(font)
        if placeholder_cn and placeholder_en:
            line.setPlaceholderText(placeholder_cn if chinese else placeholder_en)
        line.setEnabled(enabled)
        if row is not None and col is not None:
            layout.addWidget(line, row, col, 1, colspan)
        return line

    layout = QGridLayout()# 1. 增加控件间距，提供呼吸感
    layout.setVerticalSpacing(25) 
    layout.setHorizontalSpacing(20)
    layout.setContentsMargins(30, 30, 30, 30) # 增加四周留白
    layout.setSpacing(20)

    # Row 1: 数据类型 & 数据名称
    create_label('数据类型', 'Type', 1, 0)
    main_win.data_type_combo = create_combo([gt[0] for gt in gnss_type], 1, 1)
    main_win.data_type_combo.textActivated[str].connect(lambda: dataTypeOnActivated(main_win))

    create_label('数据名称', 'Name', 1, 3)
    main_win.name_type_combo = create_combo(gnss_type[0][1], 1, 4)
    main_win.name_type_combo.textActivated[str].connect(lambda: nameTypeOnActivated(main_win))

    # Row 2: 年份 & 月份
    create_label('下载年份', 'Year', 2, 0)
    main_win.year_line = create_line_edit(row=2, col=1)

    create_label('下载月份', 'Month', 2, 3)
    main_win.month_line = create_line_edit("无需填写", "Input not required.", False, 2, 4)

    # Row 3: 起始日 & 截止日
    create_label('起始日', 'Start Doy', 3, 0)
    main_win.begin_doy_line = create_line_edit(row=3, col=1)

    create_label('截止日', 'End Doy', 3, 3)
    main_win.end_doy_line = create_line_edit("仅下载单天数据时,无需填写此项", "No fill for 1-day download.", True, 3, 4)

    # Row 4: 产品更名 & 小时选择
    create_label('产品更名', 'Rename', 4, 0)
    main_win.pro_name_line = create_line_edit("若无更名需求,无需填写此项 [3char]", "No fill if not needed. [3char]", True, 4, 1)

    create_label('小时选择', 'Hour', 4, 3)
    hour_items = [str(i) for i in range(24)] + ['0-23']
    main_win.hour_combo = create_combo(hour_items, 4, 4)

    # Row 5: 是否解压 & 多线程数
    create_label('是否解压', 'Unzip', 5, 0)
    unzip_items = ['是', '否'] if chinese else ['yes', 'no']
    main_win.unzip_combo = create_combo(unzip_items, 5, 1)

    create_label('多线程数', 'Thread', 5, 3)
    pool_items = [str(i) for i in range(1, 13)]
    main_win.pool_combo = create_combo(pool_items, 5, 4, current_index=4)

    # Row 6: 站点列表
    create_label('站点列表', 'Site', 6, 0)
    main_win.site_file_line = create_line_edit(
        "按右侧按钮选择站点文件,或输入站点名称,按逗号分开 [bjfs,abpo]",
        "Select site files, or input site names separated by ',' [bjfs,abpo].",
        True, 6, 1, 4
    )
    
    open_site_file_btn = QPushButton('  ...  ', main_win)
    open_site_file_btn.setFont(font)
    open_site_file_btn.setMinimumSize(QSize(80, choose_h + 15))
    open_site_file_btn.setStyleSheet(get_small_btn_style())
    open_site_file_btn.clicked.connect(lambda: choose_site_file(main_win))
    layout.addWidget(open_site_file_btn, 6, 5, alignment=Qt.AlignRight)

    # Row 7: 下载位置
    create_label('下载位置', 'Directory', 7, 0)
    main_win.out_dir_line = create_line_edit(
        "按右侧按钮选择下载文件夹,如不选择,则下载至程序所在路径",
        "Select folder on right. If not, download to program path.",
        True, 7, 1, 4
    )
    
    open_out_dir_btn = QPushButton('  ...  ', main_win)
    open_out_dir_btn.setFont(font)
    open_out_dir_btn.setMinimumSize(QSize(80, choose_h + 15))
    open_out_dir_btn.setStyleSheet(get_small_btn_style())
    open_out_dir_btn.clicked.connect(lambda: choose_out_dir(main_win))
    layout.addWidget(open_out_dir_btn, 7, 5, alignment=Qt.AlignRight)

    # Apply global download styles
    apply_download_styles(main_win)

    # 2. 为按钮区域增加额外的间距，将其与上方表单区分开
    layout.setRowMinimumHeight(8, 20) # 在第8行加一个空白缓冲带
    # Row 9: 下载 & 终止按钮
    btn_size = QSize(int(normalBtnSize * 1.5), int(normalBtnH * 1.0))
    
    dd_btn = QPushButton('下 载' if chinese else 'DOWNLOAD', main_win)
    dd_btn.setFont(font_big)
    dd_btn.setMinimumSize(btn_size)
    dd_btn.setStyleSheet(get_primary_btn_style())
    dd_btn.clicked.connect(lambda: dd(main_win))
    layout.addWidget(dd_btn, 9, 1, 1, 2, alignment=Qt.AlignCenter)

    kill_btn = QPushButton('终 止' if chinese else 'STOP', main_win)
    kill_btn.setFont(font_big)
    kill_btn.setMinimumSize(btn_size)
    kill_btn.setStyleSheet(get_primary_btn_style())
    kill_btn.clicked.connect(lambda: kill_p(main_win))
    layout.addWidget(kill_btn, 9, 3, 1, 2, alignment=Qt.AlignCenter)

    # Layout container
    right_top_frame = QFrame()
    right_top_frame.setObjectName("FormCard") # 方便 QSS 针对性设置
    right_top_frame.setLayout(layout)

    # 日志区域
    main_win.logPrint = QTextEdit()
    main_win.logPrint.document().setMaximumBlockCount(50)
    main_win.logPrint.setLineWrapMode(QTextEdit.NoWrap)
    main_win.logPrint.setTextInteractionFlags(Qt.TextSelectableByMouse)
    main_win.logPrint.setReadOnly(True)
    main_win.logPrint.setFont(font_big)
    main_win.logPrint.setStyleSheet(get_log_style())

    # Print initial info
    printLog(main_win, f'FAST Version : {lastVersion}')
    printLog(main_win, f'Compilation Date : {lastVersionTime}')
    printLog(main_win, 'Email : chuntaochang@whu.edu.cn')

    # 4. 调整 Splitter 比例，让日志框显得更修长美观
    splitter = QSplitter(Qt.Vertical)
    splitter.setHandleWidth(2) # 将拖动条变细，显得更精致
    splitter.setStyleSheet("QSplitter::handle { background-color: #313244; }")
    
    splitter.addWidget(right_top_frame)
    splitter.addWidget(main_win.logPrint)
    splitter.setSizes([600, 200]) # 根据你的窗体高度设置合理的默认比例

    return splitter
